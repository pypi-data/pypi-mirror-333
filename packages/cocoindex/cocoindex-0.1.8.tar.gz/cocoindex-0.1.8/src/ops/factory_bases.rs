use std::fmt::Debug;
use std::hash::Hash;
use std::sync::Arc;

use anyhow::Result;
use axum::async_trait;
use serde::de::DeserializeOwned;
use serde::Serialize;

use super::interface::*;
use super::registry::*;
use crate::base::schema::*;
use crate::base::spec::*;
use crate::setup;
// SourceFactoryBase
#[async_trait]
pub trait SourceFactoryBase: SourceFactory + Send + Sync + 'static {
    type Spec: DeserializeOwned + Send + Sync;

    fn name(&self) -> &str;

    fn get_output_schema(
        &self,
        spec: &Self::Spec,
        context: &FlowInstanceContext,
    ) -> Result<EnrichedValueType>;

    async fn build_executor(
        self: Arc<Self>,
        spec: Self::Spec,
        context: Arc<FlowInstanceContext>,
    ) -> Result<Box<dyn SourceExecutor>>;

    fn register(self, registry: &mut ExecutorFactoryRegistry) -> Result<()>
    where
        Self: Sized,
    {
        registry.register(
            self.name().to_string(),
            ExecutorFactory::Source(Arc::new(self)),
        )
    }
}

impl<T: SourceFactoryBase> SourceFactory for T {
    fn build(
        self: Arc<Self>,
        spec: serde_json::Value,
        context: Arc<FlowInstanceContext>,
    ) -> Result<(
        EnrichedValueType,
        ExecutorFuture<'static, Box<dyn SourceExecutor>>,
    )> {
        let spec: T::Spec = serde_json::from_value(spec)?;
        let output_schema = self.get_output_schema(&spec, &context)?;
        let executor = self.build_executor(spec, context);
        Ok((output_schema, executor))
    }
}

// SimpleFunctionFactoryBase

#[async_trait]
pub trait SimpleFunctionFactoryBase: SimpleFunctionFactory + Send + Sync + 'static {
    type Spec: DeserializeOwned + Send + Sync;

    fn name(&self) -> &str;

    fn get_output_schema(
        &self,
        spec: &Self::Spec,
        input_schema: &Vec<OpArgSchema>,
        context: &FlowInstanceContext,
    ) -> Result<EnrichedValueType>;

    async fn build_executor(
        self: Arc<Self>,
        spec: Self::Spec,
        input_schema: Vec<OpArgSchema>,
        context: Arc<FlowInstanceContext>,
    ) -> Result<Box<dyn SimpleFunctionExecutor>>;

    fn register(self, registry: &mut ExecutorFactoryRegistry) -> Result<()>
    where
        Self: Sized,
    {
        registry.register(
            self.name().to_string(),
            ExecutorFactory::SimpleFunction(Arc::new(self)),
        )
    }
}

impl<T: SimpleFunctionFactoryBase> SimpleFunctionFactory for T {
    fn build(
        self: Arc<Self>,
        spec: serde_json::Value,
        input_schema: Vec<OpArgSchema>,
        context: Arc<FlowInstanceContext>,
    ) -> Result<(
        EnrichedValueType,
        ExecutorFuture<'static, Box<dyn SimpleFunctionExecutor>>,
    )> {
        let spec: T::Spec = serde_json::from_value(spec)?;
        let output_schema = self.get_output_schema(&spec, &input_schema, &context)?;
        let executor = self.build_executor(spec, input_schema, context);
        Ok((output_schema, executor))
    }
}

pub trait StorageFactoryBase: ExportTargetFactory + Send + Sync + 'static {
    type Spec: DeserializeOwned + Send + Sync;
    type Key: Debug + Clone + Serialize + DeserializeOwned + Eq + Hash + Send + Sync;
    type SetupState: Debug + Clone + Serialize + DeserializeOwned + Send + Sync;

    fn name(&self) -> &str;

    fn build(
        self: Arc<Self>,
        name: String,
        target_id: i32,
        spec: Self::Spec,
        key_fields_schema: Vec<FieldSchema>,
        value_fields_schema: Vec<FieldSchema>,
        storage_options: IndexOptions,
        context: Arc<FlowInstanceContext>,
    ) -> Result<(
        (Self::Key, Self::SetupState),
        ExecutorFuture<'static, (Arc<dyn ExportTargetExecutor>, Option<Arc<dyn QueryTarget>>)>,
    )>;

    fn check_setup_status(
        &self,
        key: Self::Key,
        desired_state: Option<Self::SetupState>,
        existing_states: setup::CombinedState<Self::SetupState>,
    ) -> Result<
        impl setup::ResourceSetupStatusCheck<Key = Self::Key, State = Self::SetupState>
            + Send
            + Sync
            + 'static,
    >;

    fn will_keep_all_existing_data(
        &self,
        name: &str,
        target_id: i32,
        desired_state: &Self::SetupState,
        existing_state: &Self::SetupState,
    ) -> Result<bool>;

    fn register(self, registry: &mut ExecutorFactoryRegistry) -> Result<()>
    where
        Self: Sized,
    {
        registry.register(
            self.name().to_string(),
            ExecutorFactory::ExportTarget(Arc::new(self)),
        )
    }
}

struct ResourceSetupStatusCheckWrapper<T: StorageFactoryBase> {
    inner:
        Box<dyn setup::ResourceSetupStatusCheck<Key = T::Key, State = T::SetupState> + Send + Sync>,
    key_json: serde_json::Value,
    state_json: Option<serde_json::Value>,
}

impl<T: StorageFactoryBase> ResourceSetupStatusCheckWrapper<T> {
    fn new(
        inner: Box<
            dyn setup::ResourceSetupStatusCheck<Key = T::Key, State = T::SetupState> + Send + Sync,
        >,
    ) -> Result<Self> {
        Ok(Self {
            key_json: serde_json::to_value(inner.key())?,
            state_json: inner
                .desired_state()
                .map(|s| serde_json::to_value(s))
                .transpose()?,
            inner,
        })
    }
}

impl<T: StorageFactoryBase> Debug for ResourceSetupStatusCheckWrapper<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        std::fmt::Debug::fmt(&self.inner, f)
    }
}

#[async_trait]
impl<T: StorageFactoryBase> setup::ResourceSetupStatusCheck for ResourceSetupStatusCheckWrapper<T> {
    type Key = serde_json::Value;
    type State = serde_json::Value;

    fn describe_resource(&self) -> String {
        self.inner.describe_resource()
    }

    fn key(&self) -> &Self::Key {
        &self.key_json
    }

    fn desired_state(&self) -> Option<&Self::State> {
        self.state_json.as_ref()
    }

    fn describe_changes(&self) -> Vec<String> {
        self.inner.describe_changes()
    }

    fn change_type(&self) -> setup::SetupChangeType {
        self.inner.change_type()
    }

    async fn apply_change(&self) -> Result<()> {
        self.inner.apply_change().await
    }
}

impl<T: StorageFactoryBase> ExportTargetFactory for T {
    fn build(
        self: Arc<Self>,
        name: String,
        target_id: i32,
        spec: serde_json::Value,
        key_fields_schema: Vec<FieldSchema>,
        value_fields_schema: Vec<FieldSchema>,
        storage_options: IndexOptions,
        context: Arc<FlowInstanceContext>,
    ) -> Result<(
        (serde_json::Value, serde_json::Value),
        ExecutorFuture<'static, (Arc<dyn ExportTargetExecutor>, Option<Arc<dyn QueryTarget>>)>,
    )> {
        let spec: T::Spec = serde_json::from_value(spec)?;
        let ((setup_key, setup_state), executors) = StorageFactoryBase::build(
            self,
            name,
            target_id,
            spec,
            key_fields_schema,
            value_fields_schema,
            storage_options,
            context,
        )?;
        Ok((
            (
                serde_json::to_value(setup_key)?,
                serde_json::to_value(setup_state)?,
            ),
            executors,
        ))
    }

    fn check_setup_status(
        &self,
        key: &serde_json::Value,
        desired_state: Option<serde_json::Value>,
        existing_states: setup::CombinedState<serde_json::Value>,
    ) -> Result<
        Box<
            dyn setup::ResourceSetupStatusCheck<Key = serde_json::Value, State = serde_json::Value>
                + Send
                + Sync,
        >,
    > {
        let key: T::Key = serde_json::from_value(key.clone())?;
        let desired_state: Option<T::SetupState> = desired_state
            .map(|v| serde_json::from_value(v.clone()))
            .transpose()?;
        let existing_states = from_json_combined_state(existing_states)?;
        let status_check =
            StorageFactoryBase::check_setup_status(self, key, desired_state, existing_states)?;
        Ok(Box::new(ResourceSetupStatusCheckWrapper::<T>::new(
            Box::new(status_check),
        )?))
    }

    fn will_keep_all_existing_data(
        &self,
        name: &str,
        target_id: i32,
        desired_state: &serde_json::Value,
        existing_state: &serde_json::Value,
    ) -> Result<bool> {
        let result = StorageFactoryBase::will_keep_all_existing_data(
            self,
            name,
            target_id,
            &serde_json::from_value(desired_state.clone())?,
            &serde_json::from_value(existing_state.clone())?,
        )?;
        Ok(result)
    }
}

fn from_json_combined_state<T: Debug + Clone + Serialize + DeserializeOwned>(
    existing_states: setup::CombinedState<serde_json::Value>,
) -> Result<setup::CombinedState<T>> {
    Ok(setup::CombinedState {
        current: existing_states
            .current
            .map(|v| serde_json::from_value(v))
            .transpose()?,
        staging: existing_states
            .staging
            .into_iter()
            .map(|v| {
                anyhow::Ok(match v {
                    setup::StateChange::Upsert(v) => {
                        setup::StateChange::Upsert(serde_json::from_value(v)?)
                    }
                    setup::StateChange::Delete => setup::StateChange::Delete,
                })
            })
            .collect::<Result<_>>()?,
    })
}
