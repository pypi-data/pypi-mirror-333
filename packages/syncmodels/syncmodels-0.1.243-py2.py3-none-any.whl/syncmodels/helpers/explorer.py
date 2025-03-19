import itertools
import re

from jinja2 import (
    Template,
    StrictUndefined,
    DebugUndefined,
    UndefinedError,
    Environment,
    meta,
)

from agptools.containers import filter_list, walk, rebuild
from agptools.helpers import parse_uri, build_uri
from agptools.logs import logger

from agptools.helpers import tf
from syncmodels.definitions import (
    GEO_THING,
    GEO_NS,
    GEO_BOUNDARIES_DB,
    GEO_GRID_THING,
    GEO_CONFIG_THING,
)


# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------


log = logger(__name__)


# ---------------------------------------------------------
# Expand particle definition Helper
# ---------------------------------------------------------


def preserve_undefineds(template, context):
    pattern = re.compile(r"(\{\{[^\{]*\}\})")
    expressions = pattern.findall(template)
    for exp in set(expressions):
        try:
            Template(exp, undefined=StrictUndefined).render(context)
        except UndefinedError:
            template = template.replace(exp, f"{{% raw %}}{exp}{{% endraw %}}")
    return template


class Xpand:
    def __init__(self, storage):
        self.storage = storage
        self.targets = {}
        self.db_uris = []

    async def explore(self, exclude=".*/(Tube.*|particle|tasks)"):
        """
        build the whole ns;//db/table uri map
        """
        if self.db_uris:
            return

        storage = self.storage.storage
        root = await storage.info()
        for ns in root["namespaces"]:
            uri = f"{ns}://"
            info = await storage.info(uri)
            for db in info["databases"]:
                uri = f"{ns}://{db}"
                log.info(uri)
                info = await storage.info(uri)
                for table in info["tables"]:
                    uri = f"{ns}://{db}/{table}"
                    if not exclude or not re.match(exclude, uri):
                        self.db_uris.append(uri)

    async def expand(self, data, unwrap=False):
        """
        walk for the data
        analyze with ((keys,), value) match some uri in map
        extract all possible parameters from matching uri
        . create a product chain to iterate for all combinations
        . temporary replacement of matching uri with the value matched
        . render all string values with jinja2 and the context generated by product iterator
        . assert jinja2 doesn't throw any exception
        the patched data is ready for extraction
        target uri is the global key (dict) that stich this particular data render
        loop

        iterate over all target uri and yield particle definitions

        """
        sources = data.get("sources")
        if not sources:
            log.error("IGNORING: definition hasn't any sources: [%s]", data)
            return

        universe = {}
        for idx, pattern in enumerate(sources):
            for uri in self.db_uris:
                # check both uris (normal and tf(uri))
                uri2 = parse_uri(uri)
                uri2["path"] = uri2["path"].replace("_", "/")
                uri2 = build_uri(**uri2)
                for _ in [uri, uri2]:
                    if m := re.match(f"{pattern}$", _):
                        d = m.groupdict()
                        item = idx, set([uri]), d
                        if d:
                            item = idx, set([uri]), d
                            universe.setdefault(idx, []).append(item)
                        else:
                            holder = universe.setdefault(idx, [item])
                            holder[0][1].update(item[1])
                        break
        # we have all candidates that match every source input
        # now we need to expand (product) them all
        collections = [samples for samples in universe.values()]

        if not collections:
            log.error("can't find any sources using these definitions")
            for idx, pattern in enumerate(sources):
                log.error("[%s]: %s", idx, pattern)
            return

        L = list(itertools.product(*collections))
        N = len(L)
        log.info("[%s] sources has been found", N)
        for idx, row in enumerate(L):
            # generate source expansion
            item = dict(data)
            ctx = {}
            # sources = item["sources"] = [None] * len(row)
            # for src in row:
            #     sources[src[0]] = src[1]
            #     ctx.update(src[2])

            sources = set()
            for src in row:
                sources.update(src[1])
                ctx.update(src[2])

            sources = item["sources"] = list(sources)
            sources.sort()

            # render all variables in the rest of the data definition
            try:

                _data = []
                # env = Environment(undefined=DebugUndefined)
                for key, value in walk(item):
                    if isinstance(value, str):
                        template = preserve_undefineds(value, ctx)
                        value = Template(template).render(**ctx)
                    #                         # let pass some undefined variables when they can't
                    #                         # be resolved if this particular moment
                    #                         ast = env.parse(value)
                    #                         needed = meta.find_undeclared_variables(ast)
                    #                         missing = needed.difference(ctx)
                    #
                    #                         kw = {
                    #                             **ctx,
                    #                             **{k: "{{ " + k + " }}" for k in missing},
                    #                         }
                    #                         template = env.from_string(value)
                    #                         _value = template.render(
                    #                             # **kw,
                    #                             undefined=DebugUndefined,
                    #                         )
                    _data.append((key, value))

                new = rebuild(_data)
                log.debug("[%s]: %s", idx, new)
                if unwrap:
                    for _ in new["sources"]:
                        yield _
                else:
                    yield new

            except Exception as why:
                log.error(why)

    async def find_geo_tubes(self, unwrap=False):
        await self.explore()

        data = {
            "sources": [r".*_geo$"],
        }

        async for new in self.expand(data, unwrap):
            yield new

#     async def find_geo_particles(self, unwrap=False):
#         await self.explore()
#
#         fqid = f"{APP_NS}://{APP_DB}/{GEO_THING}"
#
#         data = {
#             "sources": [fqid],
#         }
#
#         async for new in self.expand(data, unwrap):
#             yield new

    async def find_geo_config(self, unwrap=False):
        await self.explore()

        grid_config_uri = (
            f"{GEO_NS}://{GEO_BOUNDARIES_DB}/{GEO_CONFIG_THING}/{GEO_GRID_THING}"
        )

        data = {
            "sources": [grid_config_uri],
        }

        async for new in self.expand(data, unwrap):
            yield new
