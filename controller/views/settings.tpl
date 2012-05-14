%import lightbot

<div data-role="page" id="settings" data-theme="c">
%include header title='Settings'

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
      <!-- TODO: modify & save ambient light settings here -->
      <!-- TODO: enable/disable ambient mode -->

      <ul data-role="listview" data-inset="true">
        <li data-role="fieldcontain">
          <label for="ambient-switch">Ambient</label>
          <select id="ambient-switch" data-role="slider" name="xbmc-switch">
            <option value="off"
%if not lightbot.AMBIENT:
selected
%end
            >Off</option>
            <option value="on"
%if lightbot.AMBIENT:
selected
%end
            >On</option>
          </select>
        </li>
      </ul>

      <h3>Sensor value</h3>
      <p id="sensor-value">{{lightbot.query_sensor()}}</p>
      <!--<h3>Ambient value</h3>
      <p id="ambient-value">
%if lightbot.AMBIENT:
active
%else:
not active
%end
      </p>-->
    </div>
  </div>

%include footer page='settings'
</div>


