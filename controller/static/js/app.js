
var updateUiTimer = null;
function enableUiUpdate() {
    updateUiTimer = setInterval(function() {
        $.getJSON('/status', {"ts":new Date().getTime()}, loadStatus);
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
        $.post('/lights', {
            "action" : $(this).val(),
            "ts"     : new Date().getTime()
        }, loadLightsStatus);
    });

    $("#bright-btn").click(function() {
        disableUiUpdate();
        $.post('/lights', {
            "action" : "bright",
            "ts"     : new Date().getTime()
        }, loadLightsStatus);
    });

    $("#dim-btn").click(function() {
        disableUiUpdate();
        $.post('/lights', {
            "action" : "dim",
            "ts"     : new Date().getTime()
        }, loadLightsStatus);
    });

    $("#scene-menu").change(function() {
        if ($(this).val() != "-") {
            disableUiUpdate();
            $.post('/lights', {
                "action" : "scene",
                "scene"  : $(this).val(),
                "ts"     : new Date().getTime()
            }, function(data) {
                $("#scene-menu").val("-").selectmenu('refresh');
                loadLightsStatus(data);
            });
        }
    });

    /** Programs */
    $("#xbmc-switch").change(function() {
        disableUiUpdate();
        $.post('/programs', {
            "action"  : $(this).val(),
            "program" : "xbmc",
            "ts"      : new Date().getTime()
        }, loadProgramsStatus);
    });

    // this allows the voice dictation on iOS to work when the Done button
    // is pressed on the keyboard
    $("#keyboard-txt").change(function() {
        if (! $(this).val()) {
            return;
        }
        var sequence = "str "+$(this).val()+"\n";
        $(this).val('');
        $.post('/keyboard', {
            "sequence" : sequence,
            "ts"       : new Date().getTime()
        });
    });

    // send keyboard events through to xte
    // must have the xautomation package installed (ubuntu)
    $("#keyboard-txt").keyup(function(event) {
        var key = $(this).val();
        $(this).val('');

        var sequence = "str "+key+"\n";
        switch (event.which) {
            case  8: sequence = "key BackSpace\n"; break;
            case 13: sequence = "key Return\n"; break;
            case 32: sequence = "key Space\n"; break;
        }
        $.post('/keyboard', {
            "sequence" : sequence,
            "ts"       : new Date().getTime()
        });
    });

    $("#shutdown-btn").click(function() {
        disableUiUpdate();
        var when = $("#when").val();
        if (when == "0" && 
            ! confirm("Are you sure you want to shutdown now?")) {
            return;
        }
        $.post('/programs', {
            "action"  : "shutdown",
            "program" : "pc",
            "when"    : when,
            "ts"      : new Date().getTime()
        }, loadProgramsStatus);
    });

    $("#restart-btn").click(function() {
        disableUiUpdate();
        var when = $("#when").val();
        if (when == "0" && 
            ! confirm("Are you sure you want to restart now?")) {
            return;
        }
        $.post('/programs', {
            "action"  : "restart",
            "program" : "pc",
            "when"    : when,
            "ts"      : new Date().getTime()
        }, loadProgramsStatus);
    });

    $("#cancel-power-btn").click(function() {
        disableUiUpdate();
        if (! confirm("Cancel event?")) {
            return;
        }
        $.post('/programs', {
            "action"  : "clear",
            "program" : "power",
            "ts"      : new Date().getTime()
        }, loadProgramsStatus);
    });

    /** Settings */
    $("#scheduler-select").change(function() {
        $.post('/scheduler', {
            "name" : $(this).val(),
            "ts"   : new Date().getTime()
        }, function(data) {
            alert(data['msg']);
        });
    });
    $("#ambient-switch").change(function() {
        disableUiUpdate();
        var active = $(this).val() == "on";
        $.post('/lights', {
            "action" : "set_ambient_active",
            "active" : active,
            "ts"     : new Date().getTime()
        }, loadLightsStatus);
    });

    $("#ambient-enable-switch").change(function() {
        disableUiUpdate();
        var enabled = $(this).val() == "on";
        $.post('/lights', {
            "action" : "set_ambient",
            "enable" : enabled,
            "ts"     : new Date().getTime()
        }, loadLightsStatus);
    });

    $("#save-ambient-levels-btn").click(function() {
        disableUiUpdate();
        $.post('/lights', {
            "action"  : "save_ambient_levels", 
            "low"     : $("#low-light-txt").val(),
            "maximum" : $("#max-light-txt").val(),
            "ts"      : new Date().getTime()
        }, function(data) {
            alert("Saved settings successfully.");
            loadLightsStatus(data);
        });
    });
});

