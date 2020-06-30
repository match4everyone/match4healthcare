if (!postingFormUtil) {
  var postingFormUtil = {
    handleAppearsInMapChanged: function handleAppearsInMapChanged(event) {
      document.getElementById("id_sonstige_infos").disabled = !event.srcElement
        .checked;
    },
  };

  document.addEventListener("DOMContentLoaded", function (event) {
    let displayCheckbox = document.getElementById("id_appears_in_map");
    displayCheckbox.addEventListener("input", (event) => {
      postingFormUtil.handleAppearsInMapChanged(event);
    });
    postingFormUtil.handleAppearsInMapChanged({ srcElement: displayCheckbox });
  });
}
