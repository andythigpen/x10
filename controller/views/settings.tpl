%import lightbot
%from config import get_config

%cfg = get_config()

<div data-role="page" id="settings" data-theme="c">
%include header title='Settings'

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
      <!-- TODO: modify & save ambient light settings here -->
      <!-- TODO: enable/disable ambient mode -->

      <h3>Ambient Lights</h3>
      <ul data-role="listview" data-inset="true">
        <li data-role="fieldcontain">
          <label for="ambient-enable-switch">Enabled</label>
          <select id="ambient-enable-switch" data-role="slider">
            <option value="off"
%if not cfg.getboolean('ambient', 'enabled'):
selected
%end
            >Off</option>
            <option value="on"
%if cfg.getboolean('ambient', 'enabled'):
selected
%end
            >On</option>
          </select>

        </li>
        <li data-role="fieldcontain" class="ui-grid-a">
          <label for="low-light-txt" class="ui-block-a">Low</label>
          <input class="ui-block-b" type="text" name="low-light-txt" id="low-light-txt" value="{{ cfg.get('ambient', 'low') }}" />
          <br style="clear:both;"/>
        </li>
        <li data-role="fieldcontain" class="ui-grid-a">
          <label for="high-light-txt" class="ui-block-a">High</label>
          <input class="ui-block-b" type="text" name="high-light-txt" id="high-light-txt" value="{{ cfg.get('ambient', 'high') }}" />
          <br style="clear:both;"/>
        </li>
        <li data-role="fieldcontain" class="ui-grid-a">
          <label for="max-light-txt" class="ui-block-a">Max</label>
          <input class="ui-block-b" type="text" name="max-light-txt" id="max-light-txt" value="{{ cfg.get('ambient', 'max') }}" />
          <br style="clear:both;"/>
        </li>
      </ul>
      <a href="#" data-role="button" id="save-ambient-levels-btn">Save</a>

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


