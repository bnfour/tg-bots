<div class="bot-list">
    <%
        for bot in data:
            include('bot.tpl', bot=bot)
        end
    %>
</div>
