%import lightbot

<div data-role="page" id="settings" data-theme="c">
%include header title='Settings'

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
        <!-- TODO: modify & save ambient light settings here -->
        <!-- TODO: enable/disable ambient mode -->
        <h3>Sensor value</h3>
        <p id="sensor-value">{{lightbot.query_sensor()}}</p>
        <h3>Ambient value</h3>
        <p id="ambient-value">
%if lightbot.AMBIENT:
active
%else:
not active
%end
        </p>
    </div>
  </div>

%include footer page='settings'
</div>


