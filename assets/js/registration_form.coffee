$ = jQuery
$ ->
    $("#id_email").on('blur', (e) =>
        removeSuggestions = (element) ->
            $(element).parent().find(".help-block").remove()
        $(e.currentTarget).mailcheck
            suggested: (element, suggestion) ->
                removeSuggestions element
                suggestedLink = $("<a href='#'>").text(suggestion.full)
                suggestedLink.on('click', =>
                    $("#id_email").val(suggestion.full)
                    removeSuggestions element
                    false
                )
                $("<span class='help-block'/>")
                    .text("Did you mean ").append(suggestedLink).append("?")
                    .insertAfter(element)
            empty: (element) -> removeSuggestions element
        )
