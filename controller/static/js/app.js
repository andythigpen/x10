
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
    try {
        if (data['A1'] > 0) {
            $("#light-switch").val("on").slider('refresh');
        } else {
            $("#light-switch").val("off").slider('refresh');
        }
    } catch (e) {
    }
    $("#sensor-value").html(data['sensor']);
    // $("#ambient-value").html(data['ambient'] ? "active" : "not active");
    try {
        $("#ambient-switch").val(data['ambient'] ? "on" : "off").
            slider('refresh');
    } catch (e) {
    }

    if (updateUiTimer == null) {
        enableUiUpdate();
    }
}

function loadProgramsStatus(data) {
    if (data['xbmc'] != null) {
        try {
            $("#xbmc-switch").val(data['xbmc'] ? "start" : "stop").
                slider('refresh');
        } catch (e) {
        }
    }
    if (data['power'] != null) {
        $("#power-status").html(data['power']);
        if (data['power'] != '') {
            $("#cancel-power-btn").show();
        }
        else {
            $("#cancel-power-btn").hide();
        }
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

    /** Lights */
    $("#light-switch").change(function() {
        disableUiUpdate();
        $.post('/lights', {"action": $(this).val()}, loadLightsStatus);
    });

    $("#bright-btn").click(function() {
        disableUiUpdate();
        $.post('/lights', {"action": "bright"}, loadLightsStatus);
    });

    $("#dim-btn").click(function() {
        disableUiUpdate();
        $.post('/lights', {"action": "dim"}, loadLightsStatus);
    });

    $("#scene-menu").change(function() {
        if ($(this).val() != "-") {
            disableUiUpdate();
            $.post('/lights', {"action": "scene", "arg":$(this).val()}, 
                loadLightsStatus);
        }
    });

    /** Programs */
    $("#xbmc-switch").change(function() {
        disableUiUpdate();
        $.post('/programs', {"action": $(this).val(), "program":"xbmc"}, 
            loadProgramsStatus);
    });

    $("#shutdown-btn").click(function() {
        disableUiUpdate();
        var when = $("#when").val();
        if (when == "0" && 
            ! confirm("Are you sure you want to shutdown now?")) {
            return;
        }
        $.post('/programs', {"action":"shutdown", "program":"pc", "arg":when}, 
            loadProgramsStatus);
    });

    $("#restart-btn").click(function() {
        disableUiUpdate();
        var when = $("#when").val();
        if (when == "0" && 
            ! confirm("Are you sure you want to shutdown now?")) {
            return;
        }
        $.post('/programs', {"action":"reboot", "program":"pc", "arg":when}, 
            loadProgramsStatus);
    });

    $("#cancel-power-btn").click(function() {
        disableUiUpdate();
        if (! confirm("Cancel event?")) {
            return;
        }
        $.post('/programs', {"action":"clear", "program":"power"},
            loadProgramsStatus);
    });

    /** Settings */
    $("#ambient-switch").change(function() {
        disableUiUpdate();
        var enabled = $(this).val() == "on";
        $.post('/lights', {"action": "set_ambient", "arg": enabled}, 
            loadLightsStatus);
    });
});

