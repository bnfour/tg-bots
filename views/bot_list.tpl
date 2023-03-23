<p>
    <%
        for bot in data:
            include('bot.tpl', bot=bot)
        end
    %>
</p>
