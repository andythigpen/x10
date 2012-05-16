%import lightbot
%import config

%cfg = config.get_config()

<div data-role="page" id="lights" data-theme="c">
%include header title="Lights"

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">

      <ul data-role="listview" data-inset="true">
        <li data-role="fieldcontain">
          <label for="light-switch">Lights</label>
          <select id="light-switch" data-role="slider" name="xbmc-switch">
            <option value="off"
%if lightbot.status()[lightbot.LIVING_ROOM+lightbot.LIGHTS] == 0:
selected
%end
            >Off</option>
            <option value="on"
%if lightbot.status()[lightbot.LIVING_ROOM+lightbot.LIGHTS] > 0:
selected
%end
            >On</option>
          </select>
        </li>
        <li data-role="fieldcontain">
          <label for="ambient-switch">Sensor Active</label>
          <select id="ambient-switch" data-role="slider" name="ambient-switch">
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
      
      <div data-role="fieldcontain">
        <div data-role="controlgroup">
          <a href="#" id="bright-btn" data-role="button" data-icon="arrow-u">Brighten</a>
          <a href="#" id="dim-btn" data-role="button" data-icon="arrow-d">Dim</a>
        </div>
      </div>

      <!-- <div data-role="fieldcontain"> -->
      <!--   <fieldset data-role="controlgroup"> -->
      <!--     <label for="dimmer">Dimmer:</label> -->
      <!--       <input type="range" name="dimmer" id="dimmer" value="0" min="0" max="24" step="2" data-highlight="false" /> -->
      <!--   </fieldset> -->
      <!-- </div> -->

      <div data-role="fieldcontain">
        <label for="scene-menu">Ambient (night)</label>
        <select name="scene-menu" id="scene-menu">
          <option value="-">---</option>
%for scene,value in cfg.items('scenes'):
<option value="{{ scene }}">{{ scene.capitalize() }}</option>
%end
          <!--<option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>-->
        </select>
      </div>
    </div>
  </div>

%include footer page='lights'
</div>


