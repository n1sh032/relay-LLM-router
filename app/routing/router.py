from app.providers.base import Provider, ChatRequest, ChatResponse

# just a rough list for now of which errors mean "try someone else"
# vs which ones mean "this is genuinely broken, dont bother retrying"
# gonna refine this as i learn more about what each sdk actually throws

class AllProvidersFailedError(Exception):
    # raised when literally every provider in the list failed
    pass


# maps a quality level to (which provider to try first, which model to use)
