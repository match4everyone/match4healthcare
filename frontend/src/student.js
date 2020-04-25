import $ from 'jquery'
import { ProfileHelper } from './student/ProfileHelper.mjs'


document.addEventListener('DOMContentLoaded', function() {
    let helper = new ProfileHelper()
    let qualifikationSelectors = document.querySelectorAll('div.ausbildung-checkbox input')
    qualifikationSelectors.forEach(element => {
        element.addEventListener('change', (event) => helper.handleQualificationInput(event) )
        // To handle Mozillas brilliant idea to keep state of checkboxes on refresh, trigger dummy handler for every checkbox
        helper.handleQualificationInput({ srcElement: element })
    })        
    $('#id_availability_start').attr('type', 'date')
})