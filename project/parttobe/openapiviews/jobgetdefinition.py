import parttobe.openapiviews.helpers as helpers
import collections

arguments = collections.namedtuple(
    "JobGetArgumentsType",
    [
        "id",
        "respond_200",
    ],
)

responders = {
    "200": helpers.get_body_constructor("job:get", "200"),
}
