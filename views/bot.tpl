% if bot.is_online is None:
    <span>more to come?</span>
% else:
    % if bot.is_online:
        <span><a href="https://t.me/{{bot.username}}">@{{bot.username}}</a></span>
    % else:
        <span>N/A</span>
    % end
% end
