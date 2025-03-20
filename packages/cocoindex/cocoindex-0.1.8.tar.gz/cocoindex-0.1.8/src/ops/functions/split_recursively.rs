use regex::Regex;
use std::sync::LazyLock;
use std::{collections::HashMap, sync::Arc};

use crate::base::field_attrs;
use crate::{fields_value, ops::sdk::*};

#[derive(Debug, Deserialize)]
pub struct Spec {
    #[serde(default)]
    language: Option<String>,

    chunk_size: usize,

    #[serde(default)]
    chunk_overlap: usize,
}

static DEFAULT_SEPARATORS: LazyLock<Vec<Regex>> = LazyLock::new(|| {
    [r"\n\n+", r"\n", r"\s+"]
        .into_iter()
        .map(|s| Regex::new(s).unwrap())
        .collect()
});
static SEPARATORS_BY_LANG: LazyLock<HashMap<&'static str, Vec<Regex>>> = LazyLock::new(|| {
    [
        (
            "markdown",
            vec![
                r"(^|\n)\n*# ",
                r"(^|\n)\n*## ",
                r"(^|\n)\n*### ",
                r"(^|\n)\n*#### ",
                r"(^|\n)\n*##### ",
                r"(^|\n)\n*###### ",
                // Code block
                r"(^|\n\n)\n*```\S*\n|\n\s*```\n*(\n\n|$)",
                // Horizontal lines
                r"(^|\n\n)\n*(\*\*\*+|---+|___+)\n*(\n\n|$)",
                r"\n\n+",
                r"(\.|!|\?)\s*(\s|$)",
                r":\s*(\s|$)",
                r";\s*(\s|$)",
                r"\n",
                r"\s+",
            ],
        ),
        (
            "python",
            vec![
                // First, try to split along class definitions
                r"\nclass ",
                r"\n  def ",
                r"\n    def ",
                r"\n      def ",
                r"\n        def ",
                // Now split by the normal type of lines
                r"\n\n",
                r"\n",
                r"\s+",
            ],
        ),
        (
            "javascript",
            vec![
                // Split along function definitions
                r"\nfunction ",
                r"\nconst ",
                r"\nlet ",
                r"\nvar ",
                r"\nclass ",
                // Split along control flow statements
                r"\n\s*if ",
                r"\n\s*for ",
                r"\n\s*while ",
                r"\n\s*switch ",
                r"\n\s*case ",
                r"\n\s*default ",
                // Split by the normal type of lines
                r"\n\n",
                r"\n",
            ],
        ),
    ]
    .into_iter()
    .map(|(lang, separators)| {
        let regexs = separators
            .into_iter()
            .map(|s| Regex::new(s).unwrap())
            .collect();
        (lang, regexs)
    })
    .collect()
});

struct Executor {
    spec: Spec,
    separators: &'static [Regex],
}

impl Executor {
    fn new(spec: Spec) -> Result<Self> {
        let separators = spec
            .language
            .as_ref()
            .and_then(|lang| {
                SEPARATORS_BY_LANG
                    .get(lang.to_lowercase().as_str())
                    .map(|v| v.as_slice())
            })
            .unwrap_or(DEFAULT_SEPARATORS.as_slice());
        Ok(Self { spec, separators })
    }

    fn add_output<'s>(pos: usize, text: &'s str, output: &mut Vec<(RangeValue, &'s str)>) {
        if !text.trim().is_empty() {
            output.push((RangeValue::new(pos, pos + text.len()), text));
        }
    }

    fn split_substring<'s>(
        &self,
        s: &'s str,
        base_pos: usize,
        next_sep_id: usize,
        output: &mut Vec<(RangeValue, &'s str)>,
    ) {
        if next_sep_id >= self.separators.len() {
            Self::add_output(base_pos, s, output);
            return;
        }

        let flush_small_chunks =
            |chunks: &[RangeValue], output: &mut Vec<(RangeValue, &'s str)>| {
                if chunks.is_empty() {
                    return;
                }
                let mut start_pos = chunks[0].start;
                for i in 1..chunks.len() - 1 {
                    let chunk = &chunks[i];
                    if chunk.end - start_pos > self.spec.chunk_size {
                        Self::add_output(base_pos + start_pos, &s[start_pos..chunk.end], output);

                        // Find the new start position, allowing overlap within the threshold.
                        let mut new_start_idx = i + 1;
                        let next_chunk = &chunks[i + 1];
                        while new_start_idx > 0 {
                            let prev_pos = chunks[new_start_idx - 1].start;
                            if prev_pos <= start_pos
                                || chunk.end - prev_pos > self.spec.chunk_overlap
                                || next_chunk.end - prev_pos > self.spec.chunk_size
                            {
                                break;
                            }
                            new_start_idx -= 1;
                        }
                        start_pos = chunks[new_start_idx].start;
                    }
                }

                let last_chunk = &chunks[chunks.len() - 1];
                Self::add_output(base_pos + start_pos, &s[start_pos..last_chunk.end], output);
            };

        let mut small_chunks = Vec::new();
        let mut process_chunk = |start: usize, end: usize| {
            let chunk = &s[start..end];
            if chunk.len() <= self.spec.chunk_size {
                small_chunks.push(RangeValue::new(start, start + chunk.len()));
            } else {
                flush_small_chunks(&small_chunks, output);
                small_chunks.clear();
                self.split_substring(chunk, base_pos + start, next_sep_id + 1, output);
            }
        };

        let mut next_start_pos = 0;
        for cap in self.separators[next_sep_id].find_iter(s) {
            process_chunk(next_start_pos, cap.start());
            next_start_pos = cap.end();
        }
        if next_start_pos < s.len() {
            process_chunk(next_start_pos, s.len());
        }

        flush_small_chunks(&small_chunks, output);
    }
}

fn translate_bytes_to_chars<'a>(text: &str, offsets: impl Iterator<Item = &'a mut usize>) {
    let mut offsets = offsets.collect::<Vec<_>>();
    offsets.sort_by_key(|o| **o);

    let mut offsets_iter = offsets.iter_mut();
    let mut next_offset = if let Some(offset) = offsets_iter.next() {
        offset
    } else {
        return;
    };

    let mut char_idx = 0;
    for (bytes_idx, _) in text.char_indices() {
        while **next_offset == bytes_idx {
            **next_offset = char_idx;
            next_offset = if let Some(offset) = offsets_iter.next() {
                offset
            } else {
                return;
            }
        }
        char_idx += 1;
    }

    // Offsets after the last char.
    for offset in offsets_iter {
        **offset = char_idx;
    }
}

#[async_trait]
impl SimpleFunctionExecutor for Executor {
    async fn evaluate(&self, input: Vec<Value>) -> Result<Value> {
        let str_value = input.into_iter().next().unwrap();
        let str_value = str_value.as_str().unwrap();

        let mut output = Vec::new();
        self.split_substring(str_value, 0, 0, &mut output);

        translate_bytes_to_chars(
            str_value,
            output
                .iter_mut()
                .map(|(range, _)| [&mut range.start, &mut range.end].into_iter())
                .flatten(),
        );

        let table = output
            .into_iter()
            .map(|(range, text)| (range.into(), fields_value!(Arc::<str>::from(text)).into()))
            .collect();

        Ok(Value::Table(table))
    }
}

pub struct Factory;

#[async_trait]
impl SimpleFunctionFactoryBase for Factory {
    type Spec = Spec;

    fn name(&self) -> &str {
        "SplitRecursively"
    }

    fn get_output_schema(
        &self,
        _spec: &Spec,
        input_schema: &Vec<OpArgSchema>,
        _context: &FlowInstanceContext,
    ) -> Result<EnrichedValueType> {
        match &expect_input_1(input_schema)?.value_type.typ {
            ValueType::Basic(BasicValueType::Str) => {}
            t => {
                api_bail!("Expect String as input type, got {}", t)
            }
        }
        Ok(make_output_type(CollectionSchema::new(
            CollectionKind::Table,
            vec![
                FieldSchema::new("location", make_output_type(BasicValueType::Range)),
                FieldSchema::new("text", make_output_type(BasicValueType::Str)),
            ],
        ))
        .with_attr(
            field_attrs::CHUNK_BASE_TEXT,
            serde_json::to_value(&input_schema[0].analyzed_value)?,
        ))
    }

    async fn build_executor(
        self: Arc<Self>,
        spec: Spec,
        _input_schema: Vec<OpArgSchema>,
        _context: Arc<FlowInstanceContext>,
    ) -> Result<Box<dyn SimpleFunctionExecutor>> {
        Ok(Box::new(Executor::new(spec)?))
    }
}
