### General Rules

- All Tecton data types (e.g. `Float64`, `Int64`, `Timestamp`), `Field` and `Attribute` should be imported from the submodule `tecton.types`. You must not try to import them from `tecton` directly
- `Aggregate` must be imported from `tecton` directly, not from any submodule of `tecton`. You must never set a `column` parameter on an Aggregate class. The right parameter is called `input_column`. `input_column` expects a tecton.types.Field instance
- The function name for average is `mean`, not `avg`
- In any Tecton object or decorator
    - `schema` parameter should be an array of Tecton `Field` instances
    - `join_keys` parameter should be an array of Tecton `Field` instances
    - `entities` parameter should be an array of Tecton `Entity` instances
    - `features` parameter should be an array of Tecton `Aggregate`, `Attribute`, `Embedding` or `Calculation` instances
- When creating a feature view, you should always use on of the decorators: `@batch_feature_view`, `@stream_feature_view`, `@realtime_feature_view`. You should never directly use `BatchFeatureView`, `StreamFeatureView`, `RealTimeFeatureView` to declare a feature view
- There shouldn't be any python type annotations in tecton decorated functions.
- `mode` must be set when defining a feature view, here are the rules:
    - For a realtime feature view, it should be `pandas` or `python`. 
    - For a stream feature view that uses Spark, it should be `spark_sql` or `PySpark`. 
    - For a stream feature view that uses Rift, it should be `pandas` or `python`.
    - For a batch feature view that uses Spark, it should be `spark_sql` or `PySpark`. 
    - For a batch feature view that uses Rift, it should be `pandas` or `python`.
- When you define a feature view, you must make sure that the language you use in your decorated function matches the mode you set on the feature view. For example, if the mode is sparksql, you must return a string of sparksql. if the mode is pyspark, you must return a pyspark dataframe. if the mode is pandas, you must return a pandas dataframe. if the mode is python, you must return a python object
- Don't ever create features that depend on classes from a _compat tecton sub module


### SQL Translation Rules

- When translating a SQL to a feature view, you should first check if the top level SQL contains any aggregation, including window aggregations.
    - If it does, translate the aggregation part to Tecton `Aggregate` expressions and put them into the feature view decorator, and you must also rewrite the SQL to remove the aggregation part and then put the rewritten SQL into the decorated function.
    - If the top level SQL doesn't contain any aggregation, then you should put the entire SQL into the transformation function and use `Attribute` expressions in the feature view decorator.
- When translating a SQL to a feature view, you must check if a timestamp field is specified in the SQL.
    - If it is, you must set the `timestamp_field` parameter on the feature view decorator. And if rewriting the SQL, the timestamp field must be included in the rewritten SQL.
    - If not, you should stop working and ask the user to modify the SQL to include a timestamp field
- When translating a SQL to a feature view, unless specified by the user, you should assume that you need to create the data source (tables) and the entity used in the SQL


### Time & Period Arguments Rules

- Any time or period related arguments should be specified using either `datetime` or `timedelta` (remember to import them from the datetime module)
- The `aggregation_interval` is required for feature views with aggregations. And must be set to at least 60 seconds for feature views with aggregations
- The `batch_schedule` must be an integer multiple of the `aggregation_interval`
- The `feature_start_time` parameter is required for feature views with materialization enabled
- The `ttl` parameter should NOT be set for feature views with aggregations
- The `batch_schedule` must be set to at least 1 hour



### Stream Feature Rules

- The `source` parameter of a stream feature view must be a `StreamSource`.
- If you see the error `Field schema is required for a StreamSource with a PushConfig` means that you must specify the parameter `schema` on the class `StreamSource`. Schema is an array of `tecton.types.Field` instances
- `PushConfig` can be used in a stream feature view ONLY WHEN Rift compute is supported
- The field `schema` is required for a `StreamSource` if and only if you set the stream_config to a `PushConfig`.
- The `schema` parameter is not allowed for `KafkaConfig` or `KinesisConfig`, you must not set it

### Realtime Feature Rules

- `OnDemandFeatureView` has been renamed to `RealTimeFeatureView`

### Batch Feature Rules

- `timestamp_field` must be set in `@batch_feature_view` decorator

### Other Rules

- Don't create Spark FeatureViews or DataSources if Spark is not supported. If Spark is not supported, but Rift is, your only option to create streaming features is to use a StreamFeatureView with a PushConfig
- Never set a description parameter on a SnowflakeConfig

