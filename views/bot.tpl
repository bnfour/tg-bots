% if bot.is_online is None:
    <span>more to come?</span>
% else:
    % if bot.is_online:
        <a href="https://t.me/{{bot.username}}">@{{bot.username}}</a>
    % else:
        <span>N/A</span>
    % end
% end
