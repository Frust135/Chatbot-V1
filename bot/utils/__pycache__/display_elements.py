def message_options(title, options):
    """
    Creates a message activity with a hero card displaying a list of options.

    Args:
        title (str): The title of the message activity.
        options (list): A list of options to be displayed as buttons in the hero card.

    Returns:
        Activity: The message activity with the hero card.
    """
    from botbuilder.core import CardFactory
    from botbuilder.schema import (
        Activity,
        ActivityTypes,
        CardAction,
        HeroCard,
        Attachment,
    )

    card = HeroCard(
        title="Opciones",
        buttons=[
            CardAction(
                type="imBack",
                title=option,
                value=option,
            )
            for option in options
        ],
    )

    attachment = Attachment(
        content_type=CardFactory.content_types.hero_card, content=card.__dict__
    )
    message = Activity(type=ActivityTypes.message, text=title, attachments=[attachment])

    return message


def message_options_with_back(title, options, back_message="Volver"):
    """
    Creates a message activity with a hero card displaying a list of options.
    This function also adds a button to go back with the message.

    Args:
        title (str): The title of the message activity.
        options (list): A list of options to be displayed as buttons in the hero card.

    Returns:
        Activity: The message activity with the hero card.
    """
    from botbuilder.core import CardFactory
    from botbuilder.schema import (
        Activity,
        ActivityTypes,
        CardAction,
        HeroCard,
        Attachment,
    )

    card_buttons = [
        CardAction(
            type="imBack",
            title=option,
            value=option,
        )
        for option in options
    ]
    card_buttons.append(
        CardAction(type="imBack", title=back_message, value=back_message)
    )
    card = HeroCard(title=title, buttons=card_buttons)

    attachment = Attachment(
        content_type=CardFactory.content_types.hero_card, content=card.__dict__
    )
    message = Activity(type=ActivityTypes.message, text=title, attachments=[attachment])

    return message
