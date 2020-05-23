export class ProfileHelper {
    handleQualificationInput(event) {
        let qualificationSelected = event.srcElement.checked

        // Extract qualification Id from parent div with suitable class, name ausbildung-checkbox-<id>
        let qualificationId = event.srcElement.closest('div.ausbildung-checkbox').id.split('-').slice(-1)
        this.setQualificationSectionVisibility(qualificationId, qualificationSelected)
    }

    setQualificationSectionVisibility(id, setVisibility) {
        let section = document.getElementById(`div-ausbildung-${id}`)
        if (!section) return
        if (setVisibility) {
            section.classList.remove('hidden')
        } else {
            section.classList.add('hidden')
            section.querySelectorAll('input[type=\'checkbox\']').forEach( (checkbox) => checkbox.checked = false )
            section.querySelectorAll('input[type=\'text\'], select').forEach( (textbox) => textbox.value = '' )
        }

    }
}
