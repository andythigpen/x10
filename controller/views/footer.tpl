<div data-role="footer" class="nav-footer" data-position="fixed" data-id="page-footer">
  <div data-role="navbar" class="nav-footer" data-iconpos="top" >
    <ul>
      <li>
        <a href="#lights" id="footer-lights" data-icon="custom"
%if page == 'lights':
         class="ui-btn-active ui-state-persist"
%end
         >
          Lights
        </a>
      </li>
      <li>
        <a href="#programs" id="footer-programs" data-icon="custom" 
%if page == 'programs':
         class="ui-btn-active ui-state-persist"
%end
         >
          Programs
        </a>
      </li>
      <li>
        <a href="#settings" id="footer-settings" data-icon="custom"
%if page == 'settings':
         class="ui-btn-active ui-state-persist"
%end
         >
          Settings
         </a>
      </li>
    </ul>
  </div>
</div>

