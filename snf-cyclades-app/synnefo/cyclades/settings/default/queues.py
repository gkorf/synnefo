from synnefo.lib.settings.setup import Mandatory, Default

# Queues, exchanges and bindings for AMQP
#########################################

CYCLADES_AMQP_HOSTS = Mandatory(
    example_value=["amqp://username:password@host:port"],
    description="List of RabbitMQ endpoints.",
    category="snf-cyclades-queues",
)

EXCHANGE_GANETI = Default(
    default_value="ganeti",
    description=(
        "The message queue's exchange name. Notifications from "
        "Ganeti will get dispatched from this exchange."),
    export=False,
)

CYCLADES_AMQP_BACKEND = Default(
    default_value="puka",
    example_value="puka",
    description=(
        "The AMQP backend client. Currently, only 'puka' is supported."),
    export=False,
)
