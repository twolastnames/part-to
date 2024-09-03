import parttobe.openapiviews.helpers as helpers
import collections

arguments = collections.namedtuple(
    "RunPostArgumentsType",
    [
        "jobs",
        "respond_200",
    ],
)

responders = {
    "200": helpers.get_body_constructor("run:post", "200"),
}
