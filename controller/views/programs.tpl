%import programs

<div data-role="page" id="programs" data-theme="c">
%include header

  <div data-role="content" data-iscroll>
    <div style="padding-bottom:2.5em;">
      <ul data-role="listview" data-inset="true">
        <li data-role="fieldcontain">
          <label for="xbmc-switch">XBMC</label>
          <select id="xbmc-switch" data-role="slider" name="xbmc-switch">
            <option value="stop"
%if not programs.status()['xbmc']:
selected
%end
            >Off</option>
            <option value="start"
%if programs.status()['xbmc']:
selected
%end
            >On</option>
          </select>
        </li>
      </ul>

      <div data-role="fieldcontain">
        <div data-role="controlgroup">
          <a href="#" id="shutdown-btn" data-role="button">Shutdown</a>
          <a href="#" id="restart-btn" data-role="button">Restart</a>
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
        <p id="power-status"></p>
        <a href="#" id="cancel-power-btn" data-role="button" style="display:none;">Cancel</a>
      </div>
      <br /><br /><br /><br /><br />
    </div>
  </div>

%include footer page='programs'
</div>

