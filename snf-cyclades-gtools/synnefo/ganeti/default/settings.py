from synnefo.settings.setup import Setting, Mandatory, Default

# snf-cyclades-gtools settings

AMQP_HOSTS = Mandatory(
    example_value=["amqp://username:password@host:port"],
    description="List of RabbitMQ endpoints.",
    category="snf-cyclades-gtools",
)

BACKEND_PREFIX_ID = Default(
    default_value="snf-",
    example_value="my_service_name_prefix-",
    description="Ganeti instances that run on this backend and their name "
        "starts with this prefix will be considered as Synnefo managed. Thus, "
        "corresponding notifications for those instances will be pushed to the "
        "message queue.",
    category="snf-cyclades-gtools",
    export=True,
)

EXCHANGE_GANETI = Default(
    default_value="ganeti",
    description="The message queue's exchange name. Notifications from "
        "Ganeti are pushed to this exchange.",
    category="snf-cyclades-gtools",
    export=False,
)

AMQP_BACKEND = Default(
    default_value="puka",
    example_value="puka",
    description="The AMQP backend client. Currently, only 'puka' is "
        "supported.",
    category="snf-cyclades-gtools",
    export=False,
)
