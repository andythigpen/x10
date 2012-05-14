<div data-role="page" id="lights" data-theme="c">
%include header

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">

      <ul data-role="listview" data-inset="true">
        <li data-role="fieldcontain">
          <label for="light-switch">Lights</label>
          <select id="light-switch" data-role="slider" name="xbmc-switch">
            <option value="off">Off</option>
            <option value="on">On</option>
          </select>
        </li>
      </ul>

      <!-- <div data-role="fieldcontain"> -->
      <!--   <fieldset data-role="controlgroup"> -->
      <!--     <label for="dimmer">Dimmer:</label> -->
      <!--       <input type="range" name="dimmer" id="dimmer" value="0" min="0" max="24" step="2" data-highlight="false" /> -->
      <!--   </fieldset> -->
      <!-- </div> -->

      <div data-role="fieldcontain">
        <label for="scene-menu">Scenes</label>
        <select name="scene-menu" id="scene-menu">
          <option value="-">---</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
    </div>
  </div>

%include footer page='lights'
</div>

<div data-role="page" id="programs" data-theme="c">
%include header

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
      <ul data-role="listview" data-inset="true">
        <li data-role="fieldcontain">
          <label for="xbmc-switch">XBMC</label>
          <select id="xbmc-switch" data-role="slider" name="xbmc-switch">
            <option value="stop">Off</option>
            <option value="start">On</option>
          </select>
        </li>
      </ul>

      <div data-role="fieldcontain">
        <div data-role="controlgroup">
          <a href="#" data-role="button">Shutdown</a>
          <a href="#" data-role="button">Restart</a>
        </div>

        <label for="when">When:</label>
        <select name="when" id="when">
          <option value="0">Now</option>
          <option value="1">In 1 min</option>
          <option value="5">In 5 min</option>
          <option value="10">In 10 min</option>
          <option value="30">In 30 min</option>
          <option value="60">In 1 hour</option>
          <option value="120">In 2 hours</option>
          <option value="240">In 4 hours</option>
        </select>
      </div>
    </div>
  </div>

%include footer page='programs'

</div>

<div data-role="page" id="settings" data-theme="c">
%include header title='Settings'

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
        <h3>Sensor value</h3>
        <p id="sensor-value"></p>
        <h3>Ambient value</h3>
        <p id="ambient-value"></p>
    </div>
  </div>

%include footer page='settings'
</div>

%rebase layout
