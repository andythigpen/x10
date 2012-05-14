%import lightbot

<div data-role="page" id="settings" data-theme="c">
%include header title='Settings'

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
        <h3>Sensor value</h3>
        <p id="sensor-value">{{lightbot.query_sensor()}}</p>
        <h3>Ambient value</h3>
        <p id="ambient-value">{{lightbot.AMBIENT}}</p>
    </div>
  </div>

%include footer page='settings'
</div>


