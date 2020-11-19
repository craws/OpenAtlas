/*
    This is an adapted script taken from https://github.com/ouisharelabs/wikidata-autocomplete
    It's a more a proof of concept and maybe a more talented frontend programmer can replace this
    with a more OpenAtlas centered one.
*/
(function() {

    var getJSONWikidataSearchResults, timeoutSetter, wikidataSearch;
    window.availableTags = [];
    window.taglist = function() {
        var arr;
        arr = [];
        availableTags.forEach(function(item) {
            return arr.push([item.label, item.desc, item.value]);
        });
        return arr;
    };

    window.queries = {};
    window.lastQuery = "";
    window.lastQueried = "";

    $(function() {
        $("#wikidata_id").autocomplete({
            source: availableTags,
            select: function(event, ui) {
                $("#item").val(ui.item.label);
                $("#item-id").val(ui.item.id);
                $("#item-description").html(ui.item.desc);
                $("#item-icon").attr("src", "images/" + ui.item.icon);
                return false;
            }
        }).data("ui-autocomplete")._renderItem = function(ul, item) {
            return $("<li>").append("<a>" + item.label + "<br>" + item.desc + "</a>").appendTo(ul);
        };
        return $('#wikidata_id').on('keyup', function() {
            window.lastQuery = $('#wikidata_id').val();
            if (!(window.lastQuery.length < 2 || (queries[window.lastQuery] != null) || /^Q[0-9]*$/.test(window.lastQuery) || window.timeout !== null)) {
                getJSONWikidataSearchResults(window.lastQuery);
                queries[window.lastQuery] = {};
                timeoutSetter();
                return window.lastQueried = window.lastQuery;
            }
        });
    });

    window.timeout = null;
    timeoutSetter = function() {
        var f;
        window.timeout = "not null";
        f = function() {
            window.timeout = null;
            if (window.lastQueried !== window.lastQuery) {
                window.lastQueried = window.lastQuery;
                getJSONWikidataSearchResults(window.lastQuery);
                return timeoutSetter();
            }
        };
        return setTimeout(f, 500);
    };

    wikidataSearch = function(query) {
        return "https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&search=" + query + "&origin=*";
    };

    getJSONWikidataSearchResults = function(query) {
        return $.getJSON(wikidataSearch(query), function(data) {
            if (data.search != null) {
                return data.search.forEach(function(result) {
                    var formatedResult;
                    if (result.label != null) {
                        formatedResult = {
                            value: result.id,
                            label: result.label,
                            desc: result.description
                        };
                        console.log(result.id);  /* this is what we want to select */
                        availableTags.push(formatedResult);
                        return queries[query][result.id] = result;
                    }
                });
            }
        });
    };
}).call(this);
