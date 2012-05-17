%import lightbot
%from config import get_config
%from scheduler import Scheduler

%cfg = get_config()

<div data-role="page" id="settings" data-theme="c">
%include header title='Settings'

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
      <h3>Scheduler</h3>
      <select id="scheduler-select">
%active = cfg.get('scheduler', 'active')
%s = Scheduler()
%for name in s.get_event_names():
        <option value="{{ name }}"
%if name == active:
selected
%end
        >{{ name.capitalize() }}</option>
%end
      </select>

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
          <label for="max-light-txt" class="ui-block-a">Max</label>
          <input class="ui-block-b" type="text" name="max-light-txt" id="max-light-txt" value="{{ cfg.get('ambient', 'max') }}" />
          <br style="clear:both;"/>
        </li>
      </ul>
      <a href="#" data-role="button" id="save-ambient-levels-btn">Save</a>

      <h3>Sensor value</h3>
      <p id="sensor-value">{{lightbot.query_sensor()}}</p>
    </div>
  </div>

%include footer page='settings'
</div>


