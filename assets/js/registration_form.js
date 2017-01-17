import $ from 'jquery'
import Mailcheck from 'mailcheck'

$(() => {
    $('#id_email').on('blur', (e) => {
        const removeSuggestions = (element) => $(element).parent().find('.help-block').remove()
        const emailField = e.currentTarget
        Mailcheck.run({
            email: emailField.value,
            suggested: (suggestion) => {
                removeSuggestions(emailField)
                const suggestedLink = $('<a href="#">').text(suggestion.full)
                suggestedLink.on('click', () => {
                    $('#id_email').val(suggestion.full)
                    removeSuggestions(emailField)
                    return false
                })
                $('<span class="help-block"/>')
                    .text('Did you mean ')
                    .append(suggestedLink)
                    .append('?')
                    .insertAfter(emailField)
            },
            empty: (element) => removeSuggestions(element)
        })
    })
})
