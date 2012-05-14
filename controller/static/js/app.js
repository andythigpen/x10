
var updateUiTimer = null;
function enableUiUpdate() {
    updateUiTimer = setInterval(function() {
        $.getJSON('/status', loadStatus);
    }, 3000);
}

function disableUiUpdate() {
    clearInterval(updateUiTimer);
    updateUiTimer = null;
}

function loadLightsStatus(data) {
    if (data['A1'] > 0) {
        $("#light-switch").val("on").slider('refresh');
    } else {
        $("#light-switch").val("off").slider('refresh');
    }
    if (data['sensor']) {
        $("#sensor-value").html(data['sensor']);
    }
    if (data['ambient']) {
        $("#ambient-value").html(data['ambient'] ? "active" : "not active");
    }

    if (updateUiTimer == null) {
        enableUiUpdate();
    }
}

function loadProgramsStatus(data) {
    if (data['xbmc'] != null) {
        $("#xbmc-switch").val(data['xbmc'] ? "start" : "stop").
            slider('refresh');
    }

    if (updateUiTimer == null) {
        enableUiUpdate();
    }
}

function loadStatus(data) {
    loadLightsStatus(data['lights']);
    loadProgramsStatus(data['programs']);
}

$(document).ready(function() {
    enableUiUpdate();

    $("#light-switch").change(function() {
        disableUiUpdate();
        $.post('/lights', {"action": $(this).val()}, loadLightsStatus);
    });

    $("#xbmc-switch").change(function() {
        disableUiUpdate();
        $.post('/programs', {"action": $(this).val(), "program":"xbmc"}, 
            loadProgramsStatus);
    });

    $("#scene-menu").change(function() {
        if ($(this).val() != "---") {
            disableUiUpdate();
            $.post('/lights', {"action": "scene", "arg":$(this).val()}, 
                loadLightsStatus);
        }
    });
});

