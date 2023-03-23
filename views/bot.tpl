% if bot.is_online is None:
    more to come?
% else:
    % if bot.is_online:
        <a href="https://t.me/{{bot.username}}">@{{bot.username}}</a>
    % else:
        N/A
    % end
    % # we rely on the fact that the placeholder is always last,
    &middot;
% end
