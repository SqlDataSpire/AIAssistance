# atlassian

Jira and Confluence workflow skills. Requires an Atlassian (Jira/Confluence) connector or MCP server.

| Skill | Description |
| :--- | :--- |
| [`confluence-task-tracker`](./skills/confluence-task-tracker) | Projects, tasks, Blocked vs Waiting statuses, and a daily morning brief, all kept in Confluence pages. |

**Requires** a Jira/Confluence connection, such as the [Atlassian MCP server](https://www.atlassian.com/platform/remote-mcp-server) or your assistant's Atlassian connector.

**Optional config:** copy [`config.example.json`](./skills/confluence-task-tracker/config.example.json) to `.confluence-tracker.json` in your project, or to `~/.config/confluence-task-tracker/config.json`, and fill in your site, space and page IDs. Without it, the skill finds the tracker pages itself or offers to create them.
