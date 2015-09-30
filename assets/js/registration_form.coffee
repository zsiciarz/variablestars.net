Mailcheck = require('mailcheck')
$ = require('jquery')

$ ->
    $("#id_email").on 'blur', (e) =>
        removeSuggestions = (element) ->
            $(element).parent().find(".help-block").remove()
        emailField = e.currentTarget
        Mailcheck.run
            email: emailField.value
            suggested: (suggestion) ->
                removeSuggestions emailField
                suggestedLink = $("<a href='#'>").text(suggestion.full)
                suggestedLink.on 'click', =>
                    $("#id_email").val(suggestion.full)
                    removeSuggestions emailField
                    false
                $("<span class='help-block'/>")
                    .text("Did you mean ").append(suggestedLink).append("?")
                    .insertAfter(emailField)
            empty: (element) -> removeSuggestions element
