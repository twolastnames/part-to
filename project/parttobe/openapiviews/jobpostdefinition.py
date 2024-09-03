import parttobe.openapiviews.helpers as helpers
import collections

arguments = collections.namedtuple(
    "JobPostArgumentsType",
    [
        "part_to",
        "tasks",
        "respond_200",
    ],
)

responders = {
    "200": helpers.get_body_constructor("job:post", "200"),
}
