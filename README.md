
<img width="1575" height="280" alt="github-header" src="https://github.com/user-attachments/assets/6cec1ef7-0340-416e-ab81-c73fbc8ff847" />


# QuantConnect MCP Server (Fork)

> **This is a fork of the [official QuantConnect MCP Server](https://github.com/QuantConnect/quantconnect-mcp-server) with bug fixes for API response validation issues.**

## Bug Fixes

This fork includes the following fixes:

### 1. DateTime Format Validation
**Problem:** Multiple endpoints (`list_backtests`, `list_projects`, `read_project`, `read_file`) failed with schema validation errors because the API returns date-time fields in a format that doesn't match the strict ISO 8601 `format: "date-time"` validator.

```
data.backtests[0].created should match format "date-time"
```

**Solution:** Added a custom `DateTimeStr` type that relaxes JSON schema validation for datetime fields while preserving proper Python datetime parsing.

**Affected fields:** `created`, `modified`, `launched`, `stopped`, and other datetime fields across project/backtest/file/live response schemas.

### 2. Empty Parameter Set Validation
**Problem:** The `list_backtests` endpoint failed with validation errors because the API returns `parameterSet` as an empty list `[]` when there are no parameters, but the schema expected a dictionary.

```
backtests.0.parameterSet.dict[str,union[str,float,int]]
  Input should be a valid dictionary [type=dict_type, input_value=[], input_type=list]
```

**Solution:** Updated the `parameterSet` and `parameters` field types to accept `List` in addition to `Dict`.

---

## Quick Start (This Fork)

### 1. Build the Docker image
```bash
git clone <this-repo>
cd quantconnect-mcp-server
docker build -t quantconnect-mcp-local .
```

### 2. Configure your MCP client

Example for Cursor (`mcp.json`):
```json
{
  "mcpServers": {
    "quantconnect": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "QUANTCONNECT_USER_ID",
        "-e", "QUANTCONNECT_API_TOKEN",
        "quantconnect-mcp-local"
      ],
      "env": {
        "QUANTCONNECT_USER_ID": "<your_user_id>",
        "QUANTCONNECT_API_TOKEN": "<your_api_token>"
      }
    }
  }
}
```

Get your credentials at [QuantConnect API Token](https://www.quantconnect.com/docs/v2/cloud-platform/community/profile#09-Request-API-Token).

### 3. Restart your MCP client

---

## Original Documentation

For full setup instructions, Claude Desktop configuration, and other details, see the [official QuantConnect MCP Server repository](https://github.com/QuantConnect/quantconnect-mcp-server).

---

## Available Tools (64)
| Tools provided by this Server | Short Description |
| -------- | ------- |
| `read_account` | Read the organization account status. |
| `create_project` | Create a new project in your default organization. |
| `read_project` | List the details of a project or a set of recent projects. |
| `list_projects` | List the details of all projects. |
| `update_project` | Update a project's name or description. |
| `delete_project` | Delete a project. |
| `create_project_collaborator` | Add a collaborator to a project. |
| `read_project_collaborators` | List all collaborators on a project. |
| `update_project_collaborator` | Update collaborator information in a project. |
| `delete_project_collaborator` | Remove a collaborator from a project. |
| `lock_project_with_collaborators` | Lock a project so you can edit it. |
| `read_project_nodes` | Read the available and selected nodes of a project. |
| `update_project_nodes` | Update the active state of the given nodes to true. |
| `create_compile` | Asynchronously create a compile job request for a project. |
| `read_compile` | Read a compile packet job result. |
| `create_file` | Add a file to a given project. |
| `read_file` | Read a file from a project, or all files in the project if no file name is provided. |
| `update_file_name` | Update the name of a file. |
| `update_file_contents` | Update the contents of a file. |
| `patch_file` | Apply a patch (unified diff) to a file in a project. |
| `delete_file` | Delete a file in a project. |
| `create_backtest` | Create a new backtest request and get the backtest Id. |
| `read_backtest` | Read the results of a backtest. |
| `list_backtests` | List all the backtests for the project. |
| `read_backtest_chart` | Read a chart from a backtest. |
| `read_backtest_orders` | Read out the orders of a backtest. |
| `read_backtest_insights` | Read out the insights of a backtest. |
| `update_backtest` | Update the name or note of a backtest. |
| `delete_backtest` | Delete a backtest from a project. |
| `estimate_optimization_time` | Estimate the execution time of an optimization with the specified parameters. |
| `create_optimization` | Create an optimization with the specified parameters. |
| `read_optimization` | Read an optimization. |
| `list_optimizations` | List all the optimizations for a project. |
| `update_optimization` | Update the name of an optimization. |
| `abort_optimization` | Abort an optimization. |
| `delete_optimization` | Delete an optimization. |
| `authorize_connection` | Authorize an external connection with a live brokerage or data provider. |
| `create_live_algorithm` | Create a live algorithm. |
| `read_live_algorithm` | Read details of a live algorithm. |
| `list_live_algorithms` | List all your past and current live trading deployments. |
| `read_live_chart` | Read a chart from a live algorithm. |
| `read_live_logs` | Get the logs of a live algorithm. |
| `read_live_portfolio` | Read out the portfolio state of a live algorithm. |
| `read_live_orders` | Read out the orders of a live algorithm. |
| `read_live_insights` | Read out the insights of a live algorithm. |
| `stop_live_algorithm` | Stop a live algorithm. |
| `liquidate_live_algorithm` | Liquidate and stop a live algorithm. |
| `create_live_command` | Send a command to a live trading algorithm. |
| `broadcast_live_command` | Broadcast a live command to all live algorithms in an organization. |
| `upload_object` | Upload files to the Object Store. |
| `read_object_properties` | Get Object Store properties of a specific organization and key. |
| `read_object_store_file_job_id` | Create a job to download files from the Object Store and then read the job Id. |
| `read_object_store_file_download_url` | Get the URL for downloading files from the Object Store. |
| `list_object_store_files` | List the Object Store files under a specific directory in an organization. |
| `delete_object` | Delete the Object Store file of a specific organization and key. |
| `read_lean_versions` | Returns a list of LEAN versions with basic information for each version. |
| `check_initialization_errors` | Run a backtest for a few seconds to initialize the algorithm and get initialization errors if any. |
| `complete_code` | Show the code completion for a specific text input. |
| `enhance_error_message` | Show additional context and suggestions for error messages. |
| `update_code_to_pep8` | Update Python code to follow PEP8 style. |
| `check_syntax` | Check the syntax of a code. |
| `search_quantconnect` | Search for content in QuantConnect. |
| `read_mcp_server_version` | Returns the version of the QC MCP Server that's running. |
| `read_latest_mcp_server_version` | Returns the latest version of the QC MCP Server released. |

---

## Debugging

**Build from source:**
```bash
docker build -t quantconnect-mcp-local .
```

**Test with MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector uv run src/main.py
```

**Logs:** Use `print("message", file=sys.stderr)` to log to `mcp-server-quantconnect.log`.
