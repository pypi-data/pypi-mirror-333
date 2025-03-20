import csv
import json
import os
import yaml
import base64
import importlib.resources
import csv
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from rich.console import Console

console = Console()


def wav_to_base64(wav_path: str) -> str:
    """Convert a WAV file to base64 string."""
    try:
        with open(wav_path, "rb") as wav_file:
            encoded = base64.b64encode(wav_file.read()).decode("utf-8")
            return f"data:audio/wav;base64,{encoded}"
    except Exception as e:
        console.print(
            f"[yellow]Warning: Could not convert audio file {wav_path}: {e}[/yellow]"
        )
        return None


def generate_html_report(csv_path: str, output_path: str) -> str:
    # Read CSV into list of dicts
    test_runs = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_runs.append(row)

    # Convert to JSON string
    test_runs_json = json.dumps(test_runs, indent=2)

    # Read template content
    content = importlib.resources.read_text("echofire.static", "index.html")

    # Find start and end positions
    start_marker = "const TEST_RUNS_DATA = ["
    end_marker = "];"
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker, start_pos)

    if start_pos != -1 and end_pos != -1:
        # Replace everything between markers
        content = (
            content[: start_pos + len(start_marker)]
            + test_runs_json[1:-1]  # Remove [ and ] from JSON
            + content[end_pos:]
        )

    # Write output file
    with open(output_path, "w") as f:
        f.write(content)

    return output_path


def generate_html_report_old(csv_path: str, output_path: str) -> str:
    """
    Generate an HTML report from the test results CSV file.

    Args:
        csv_path: Path to the CSV file containing test results
        output_path: Path where the HTML report will be saved
    """
    # Read the CSV file
    test_data = []
    # Store audio data separately to avoid duplication, keyed by test_name and utterance index
    audio_data = {}
    # Keep track of which test names we've processed
    processed_test_audio = set()

    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse the timestamp
                if "timestamp" in row:
                    try:
                        # Keep the original timestamp string
                        row["timestamp_original"] = row["timestamp"]
                        # Parse timestamp assuming UTC
                        dt = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                        dt = dt.replace(tzinfo=timezone.utc)
                        # Convert to local time for display
                        local_dt = dt.astimezone()
                        row["date"] = local_dt.strftime("%Y-%m-%d")
                        row["time"] = local_dt.strftime("%H:%M:%S")
                    except ValueError:
                        row["date"] = "Unknown"
                        row["time"] = "Unknown"

                # Convert success to boolean
                if "success" in row:
                    row["success"] = row["success"].upper() == "TRUE"

                # Convert assertion counts to integers
                if "assertions_passed" in row:
                    try:
                        row["assertions_passed"] = int(row["assertions_passed"])
                    except ValueError:
                        row["assertions_passed"] = 0

                if "assertions_total" in row:
                    try:
                        row["assertions_total"] = int(row["assertions_total"])
                    except ValueError:
                        row["assertions_total"] = 0

                # Initialize showDetails property to false
                row["showDetails"] = False

                # Initialize activeTab property
                row["activeTab"] = "assertions"

                # Ensure system_prompt exists (even if empty)
                if "system_prompt" not in row:
                    row["system_prompt"] = ""

                # Load transcript data if available and add audio data
                transcript_path = (
                    Path(csv_path).parent
                    / row["test_name"]
                    / "runs"
                    / row["run_id"]
                    / "transcript.yaml"
                )
                try:
                    if transcript_path.exists():
                        with open(transcript_path, "r") as tf:
                            transcript_data = yaml.safe_load(tf)
                            conversation = transcript_data.get("conversation", [])

                            # Add audio data for user messages
                            utterances_dir = (
                                Path(csv_path).parent / row["test_name"] / "utterances"
                            )

                            # Only process audio files once per test name
                            if (
                                utterances_dir.exists()
                                and row["test_name"] not in processed_test_audio
                            ):
                                # Sort utterance files to match conversation order
                                utterance_files = sorted(
                                    utterances_dir.glob("utterance_*.wav")
                                )

                                # Store audio data for this test
                                for i, audio_path in enumerate(utterance_files):
                                    audio_id = f"audio_{row['test_name']}_{i}"
                                    if audio_id not in audio_data:  # Extra safety check
                                        audio_base64 = wav_to_base64(str(audio_path))
                                        if audio_base64:
                                            audio_data[audio_id] = audio_base64

                                processed_test_audio.add(row["test_name"])

                            # Add audio references to user messages
                            user_msg_index = 0
                            for msg in conversation:
                                if msg["role"] == "user":
                                    audio_id = (
                                        f"audio_{row['test_name']}_{user_msg_index}"
                                    )
                                    if audio_id in audio_data:
                                        msg["audio_id"] = audio_id
                                    user_msg_index += 1

                            row["transcript"] = conversation
                    else:
                        row["transcript"] = []
                except Exception as e:
                    console.print(
                        f"[yellow]Warning: Could not load transcript for {row['test_name']}/{row['run_id']}: {e}[/yellow]"
                    )
                    row["transcript"] = []

                test_data.append(row)
    except FileNotFoundError:
        console.print(f"[red]Error: CSV file not found at {csv_path}")
        return
    except Exception as e:
        console.print(f"[red]Error reading CSV file: {str(e)}")
        return

    # Create the HTML file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(
            """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EchoFire Test Results</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        // Store all audio data in a single object
        const audioData = """
            + json.dumps(audio_data)
            + """;
        
        // Function to initialize all audio elements in a test's transcript
        function initTestAudio(testId) {
            const detailsRow = document.getElementById('details-' + testId);
            if (!detailsRow) return;
            
            const audioElements = detailsRow.getElementsByTagName('audio');
            for (const audio of audioElements) {
                const audioId = audio.id;
                if (audioId && !audio.src && audioData[audioId]) {
                    audio.src = audioData[audioId];
                }
            }
        }

        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        echofire: {
                            50: '#f0fdfa',
                            100: '#ccfbf1',
                            200: '#99f6e4',
                            300: '#5eead4',
                            400: '#2dd4bf',
                            500: '#14b8a6',
                            600: '#0d9488',
                            700: '#0f766e',
                            800: '#115e59',
                            900: '#134e4a',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        [x-cloak] { display: none !important; }
        /* Custom audio player styling */
        audio {
            height: 24px;
            vertical-align: middle;
        }
        audio::-webkit-media-controls-panel {
            background-color: #f0fdfa;
        }
        audio::-webkit-media-controls-current-time-display,
        audio::-webkit-media-controls-time-remaining-display {
            color: #115e59;
        }
        /* Improve contrast for span colors */
        .span-internal { background-color: #0891b2; }
        .span-client { background-color: #16a34a; }
        .span-producer { background-color: #c026d3; }
        .span-consumer { background-color: #ea580c; }
        .span-error { background-color: #dc2626; }
        
        /* Duration text styling for small spans */
        .duration-text {
            position: absolute;
            color: white;
            font-weight: 600;
            padding: 0px 3px;
            background-color: rgba(0, 0, 0, 0.75);
            border-radius: 2px;
            top: -10px;
            left: 0;
            z-index: 10;
            font-size: 10px;
            line-height: 1.2;
            white-space: nowrap;
        }
        
        /* Improve text rendering */
        .timeline-text {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            letter-spacing: 0.01em;
        }
        
        /* Fixed label column for timeline */
        .timeline-label-column {
            position: sticky;
            left: 0;
            background-color: #f9fafb;
            z-index: 10;
        }
        
        /* Ensure timeline container adapts to parent width */
        .timeline-container {
            width: 100%;
            min-width: 0;
            overflow-x: auto;
        }
        
        /* Ensure timeline content doesn't shrink below usable size */
        .timeline-content {
            min-width: 600px; /* Minimum usable width */
            width: 100%;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-900">
    <!-- Hidden container for audio elements -->
    <div id="audio-container" style="display: none;"></div>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    
    <div x-data="testResults()" class="container mx-auto px-4 py-8">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-echofire-700">EchoFire Test Results</h1>
            <p class="text-gray-600">Generated on <span x-text="generatedDate"></span></p>
        </header>
        
        <div class="bg-white rounded-lg shadow-md p-4 mb-4">
            <div class="flex flex-wrap gap-x-4 gap-y-2 mb-3">
                <div class="w-auto">
                    <label class="block text-xs font-medium text-gray-700 mb-0.5">Group By</label>
                    <select x-model="groupBy" class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-echofire-500 focus:border-echofire-500">
                        <option value="global_run_id">Global Run ID</option>
                        <option value="date">Date</option>
                        <option value="test_name">Test Name</option>
                    </select>
                </div>
                
                <div class="w-auto">
                    <label class="block text-xs font-medium text-gray-700 mb-0.5">Filter</label>
                    <div class="flex items-center h-[30px]">
                        <label class="inline-flex items-center">
                            <input type="checkbox" x-model="showFailing" class="rounded text-echofire-600 focus:ring-echofire-500 h-3.5 w-3.5">
                            <span class="ml-1.5 text-sm">Failing Only</span>
                        </label>
                    </div>
                </div>
                
                <div class="w-auto">
                    <label class="block text-xs font-medium text-gray-700 mb-0.5">Date Range</label>
                    <div class="flex items-center gap-1.5">
                        <input type="date" x-model="startDate" class="w-auto px-2 py-1 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-echofire-500 focus:border-echofire-500">
                        <span class="text-xs text-gray-500">to</span>
                        <input type="date" x-model="endDate" class="w-auto px-2 py-1 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-echofire-500 focus:border-echofire-500">
                        <div class="flex gap-1.5">
                            <button @click="filterToday()" class="text-xs bg-echofire-100 text-echofire-700 px-1.5 py-0.5 rounded hover:bg-echofire-200 focus:outline-none">Today</button>
                            <button @click="clearDateFilters" class="text-xs text-gray-500 hover:text-gray-700">Clear</button>
                        </div>
                    </div>
                </div>
                
                <div class="w-auto">
                    <label class="block text-xs font-medium text-gray-700 mb-0.5">Search</label>
                    <div class="relative">
                        <input type="text" x-model="searchTerm" placeholder="Search..." class="w-48 pl-6 pr-2 py-1 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-echofire-500 focus:border-echofire-500">
                        <div class="absolute inset-y-0 left-0 pl-1.5 flex items-center pointer-events-none">
                            <svg class="h-3.5 w-3.5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <button @click="searchInfoVisible = !searchInfoVisible" class="absolute inset-y-0 right-0 pr-1.5 flex items-center">
                            <svg class="h-3 w-3 text-gray-400 hover:text-gray-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z" clip-rule="evenodd" />
                            </svg>
                        </button>
                        <div class="absolute top-full left-0 mt-1 w-48 bg-white shadow-lg rounded-md border border-gray-200 z-10 text-xs p-1.5" x-show="searchInfoVisible" @click.away="searchInfoVisible = false" x-cloak>
                            <p class="font-medium mb-0.5 text-xs">Search in these fields:</p>
                            <ul class="list-disc pl-4 space-y-0 text-xs">
                                <li>Test Name</li>
                                <li>Global Run ID</li>
                                <li>Run ID</li>
                                <li>Error Messages</li>
                                <li>Assertion Details</li>
                                <li>System Prompt</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="flex items-center text-xs gap-3">
                <div class="font-medium text-gray-700">
                    <span x-text="filteredTests.length"></span> tests 
                    (<span class="text-blue-600" x-text="passingCount"></span> passing, 
                    <span class="text-red-600" x-text="failingCount"></span> failing)
                </div>
                <template x-if="startDate || endDate">
                    <div class="text-xs text-gray-500">
                        Date: <span x-text="startDate || 'Any'"></span> to <span x-text="endDate || 'Any'"></span>
                    </div>
                </template>
                <button 
                    @click="collapseAll()" 
                    class="text-xs bg-gray-200 hover:bg-gray-300 text-gray-700 px-2 py-0.5 rounded focus:outline-none flex items-center"
                >
                    Collapse All
                </button>
                <template x-if="hasActiveFilters">
                    <button @click="clearAllFilters" class="ml-auto text-xs bg-gray-100 text-gray-700 px-1.5 py-0.5 rounded hover:bg-gray-200 focus:outline-none flex items-center">
                        <svg class="h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                        </svg>
                        Clear All Filters
                    </button>
                </template>
            </div>
        </div>
        
        <template x-if="filteredTests.length === 0">
            <div class="bg-white rounded-lg shadow-md p-6 text-center">
                <p class="text-gray-500">No tests match the current filters</p>
            </div>
        </template>
        
        <template x-if="filteredTests.length > 0">
            <div>
                <template x-for="(group, groupName) in groupedTests" :key="groupName">
                    <div class="mb-2">
                        <div @click="toggleGroup(groupName)" class="flex items-center justify-between bg-gray-100 py-1.5 px-2 rounded-t-md border border-gray-200 cursor-pointer hover:bg-gray-200">
                            <div class="flex items-center">
                                <svg :class="{'transform rotate-90': expandedGroups[groupName]}" class="w-3.5 h-3.5 mr-1.5 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                                </svg>
                                <div class="flex flex-col sm:flex-row sm:items-center">
                                    <h2 :class="{'text-base': groupBy !== 'global_run_id', 'text-sm': groupBy === 'global_run_id'}" class="font-medium text-gray-800" x-text="groupName"></h2>
                                    <template x-if="group.length > 0 && group[0].is_ci === 'True'">
                                        <div class="ml-2 inline-flex items-center text-xs bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded-full">CI</div>
                                    </template>
                                    <template x-if="groupBy === 'global_run_id' && group.length > 0 && group[0].date">
                                        <div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4">
                                            <p class="text-xs text-gray-500 sm:ml-2" x-text="group[0].date + ' ' + group[0].time"></p>
                                            <div class="text-xs text-gray-500">
                                                <template x-if="getGroupLatencyStats(group).avg !== null">
                                                    <span>
                                                        Group Avg Latency: <span class="font-medium" x-text="getGroupLatencyStats(group).avg.toFixed(2)"></span>ms
                                                        (Min: <span class="font-medium" x-text="getGroupLatencyStats(group).min.toFixed(2)"></span>ms,
                                                        Max: <span class="font-medium" x-text="getGroupLatencyStats(group).max.toFixed(2)"></span>ms)
                                                    </span>
                                                </template>
                                            </div>
                                        </div>
                                    </template>
                                </div>
                            </div>
                            <div class="flex items-center space-x-3">
                                <div class="text-xs">
                                    <span x-text="group.length"></span> tests
                                    (<span class="text-blue-600 font-medium" x-text="countPassingInGroup(group)"></span>/<span class="text-red-600 font-medium" x-text="countFailingInGroup(group)"></span>)
                                </div>
                                <button 
                                    @click.stop="collapseAllInGroup(group)" 
                                    class="text-xs px-2 py-0.5 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded focus:outline-none"
                                >
                                    Collapse All
                                </button>
                            </div>
                        </div>
                        
                        <div x-show="expandedGroups[groupName]" x-cloak class="border-l border-r border-b border-gray-200 rounded-b-md">
                            <table class="min-w-full divide-y divide-gray-200 text-sm">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th scope="col" class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                        <th scope="col" class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test Name</th>
                                        <th scope="col" class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Run ID</th>
                                        <th scope="col" class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                                        <th scope="col" class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assertions</th>
                                        <th scope="col" class="px-3 py-1.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200" id="test-rows">
                                    <template x-for="(test, index) in group" :key="index">
                                        <tr :id="'test-row-' + test.run_id" :class="{'bg-red-50': !test.success}">
                                            <td class="px-3 py-1.5 whitespace-nowrap">
                                                <span :class="test.success ? 'bg-blue-100 text-blue-800' : 'bg-red-100 text-red-800'" class="px-1.5 py-0.5 inline-flex text-xs leading-4 font-medium rounded-full">
                                                    <span x-text="test.success ? 'PASS' : 'FAIL'"></span>
                                                </span>
                                            </td>
                                            <td class="px-3 py-1.5 whitespace-nowrap text-sm font-medium text-gray-900" x-text="test.test_name"></td>
                                            <td class="px-3 py-1.5 whitespace-nowrap text-sm text-gray-500" x-text="test.run_id"></td>
                                            <td class="px-3 py-1.5 whitespace-nowrap text-sm text-gray-500" x-text="test.timestamp_original"></td>
                                            <td class="px-3 py-1.5 whitespace-nowrap text-sm text-gray-500">
                                                <span x-text="test.assertions_passed + '/' + test.assertions_total"></span>
                                            </td>
                                            <td class="px-3 py-1.5 whitespace-nowrap text-sm text-gray-500">
                                                <button @click.stop="
                                                    toggleTestDetails(test.run_id);
                                                    $nextTick(() => {
                                                        const detailsRow = document.getElementById('details-' + test.run_id);
                                                        const currentRow = document.getElementById('test-row-' + test.run_id);
                                                        if (isTestExpanded(test.run_id)) {
                                                            currentRow.after(detailsRow);
                                                            detailsRow.style.display = 'table-row';
                                                            initTestAudio(test.run_id);
                                                        } else {
                                                            detailsRow.style.display = 'none';
                                                        }
                                                    })
                                                " class="text-echofire-600 hover:text-echofire-800 focus:outline-none text-xs">
                                                    <span x-text="isTestExpanded(test.run_id) ? 'Hide' : 'Show'"></span>
                                                </button>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                                
                                <!-- Hidden details rows that will be moved into place when needed -->
                                <div style="display: none;">
                                    <template x-for="test in group" :key="test.run_id">
                                        <tr :id="'details-' + test.run_id" :class="{'bg-red-50': !test.success}" style="display: none;">
                                            <td colspan="6" class="px-0 py-0 border-t border-gray-200">
                                                <div class="mx-3 my-2 p-3 rounded-md shadow-sm bg-white border border-gray-200" :class="{'border-red-200': !test.success}">
                                                    <div class="text-xs text-gray-700">
                                                        <template x-if="test.error">
                                                            <div class="mb-2">
                                                                <span class="font-semibold text-gray-800">Error:</span>
                                                                <span class="text-red-600 font-medium" x-text="test.error"></span>
                                                            </div>
                                                        </template>
                                                        
                                                        <div class="mb-2">
                                                            <div class="border-b border-gray-200">
                                                                <nav class="-mb-px flex">
                                                                    <button @click="test.activeTab = 'assertions'" class="py-2 px-4 text-xs font-medium" :class="test.activeTab === 'assertions' ? 'border-b-2 border-echofire-500 text-echofire-600' : 'text-gray-500 hover:text-gray-700'">
                                                                        Assertions
                                                                    </button>
                                                                    <button @click="test.activeTab = 'transcript'" class="py-2 px-4 text-xs font-medium" :class="test.activeTab === 'transcript' ? 'border-b-2 border-echofire-500 text-echofire-600' : 'text-gray-500 hover:text-gray-700'">
                                                                        Conversation Transcript
                                                                    </button>
                                                                    <button @click="test.activeTab = 'latency'" class="py-2 px-4 text-xs font-medium" :class="test.activeTab === 'latency' ? 'border-b-2 border-echofire-500 text-echofire-600' : 'text-gray-500 hover:text-gray-700'">
                                                                        Latency
                                                                    </button>
                                                                    <button @click="test.activeTab = 'system_prompt'" class="py-2 px-4 text-xs font-medium" :class="test.activeTab === 'system_prompt' ? 'border-b-2 border-echofire-500 text-echofire-600' : 'text-gray-500 hover:text-gray-700'">
                                                                        System Prompt
                                                                    </button>
                                                                    <button @click="test.activeTab = 'trace'" class="py-2 px-4 text-xs font-medium" :class="test.activeTab === 'trace' ? 'border-b-2 border-echofire-500 text-echofire-600' : 'text-gray-500 hover:text-gray-700'">
                                                                        Trace
                                                                    </button>
                                                                </nav>
                                                            </div>
                                                            
                                                            <div x-show="test.activeTab === 'assertions'" x-init="test.activeTab = 'assertions'">
                                                                <template x-if="test.assertions_details">
                                                                    <div class="mt-2">
                                                                        <div class="ml-3" x-html="formatAssertions(test.assertions_details)"></div>
                                                                    </div>
                                                                </template>
                                                                <template x-if="!test.assertions_details">
                                                                    <div class="mt-2 text-gray-500 text-xs italic">No assertion details available</div>
                                                                </template>
                                                            </div>
                                                            
                                                            <div x-show="test.activeTab === 'transcript'">
                                                                <template x-if="test.transcript && test.transcript.length > 0">
                                                                    <div class="my-2">
                                                                        <span class="font-semibold text-gray-800">Conversation Transcript:</span>
                                                                        <div class="ml-3 mt-2 space-y-2">
                                                                        <template x-for="(msg, index) in test.transcript" :key="index">
                                                                            <div :class="{
                                                                                'bg-green-50 border-l-4 border-green-500': msg.role === 'assistant',
                                                                                'bg-slate-50 border-l-4 border-slate-300': msg.role === 'user',
                                                                                'bg-amber-50 border-l-4 border-amber-400': msg.role === 'system'
                                                                            }" class="p-2 rounded">
                                                                                <div class="flex items-center gap-2 mb-1">
                                                                                    <span :class="{
                                                                                        'text-green-700 font-semibold': msg.role === 'assistant',
                                                                                        'text-slate-600': msg.role === 'user',
                                                                                        'text-amber-700': msg.role === 'system'
                                                                                    }" class="text-xs" x-text="
                                                                                        msg.role === 'assistant' ? 'Assistant' :
                                                                                        msg.role === 'user' ? 'User' :
                                                                                        'System'
                                                                                    "></span>
                                                                                    <span class="text-xs text-gray-400" x-text="msg.timestamp"></span>
                                                                                    <template x-if="msg.role === 'user' && msg.audio_id">
                                                                                        <audio 
                                                                                            :id="msg.audio_id"
                                                                                            class="h-6 ml-2"
                                                                                            controls
                                                                                        >
                                                                                            Your browser does not support the audio element.
                                                                                        </audio>
                                                                                    </template>
                                                                                </div>
                                                                                <div :class="{
                                                                                    'text-green-900': msg.role === 'assistant',
                                                                                    'text-slate-800': msg.role === 'user',
                                                                                    'text-amber-900': msg.role === 'system'
                                                                                }" class="text-sm" x-text="msg.text"></div>
                                                                            </div>
                                                                        </template>
                                                                    </div>
                                                                </template>
                                                                <template x-if="!test.transcript || test.transcript.length === 0">
                                                                    <div class="mt-2 text-gray-500 text-xs italic">No conversation transcript available</div>
                                                                </template>
                                                            </div>
                                                            
                                                            <div x-show="test.activeTab === 'latency'">
                                                                <div class="my-2">
                                                                    <div class="ml-3 mt-2">
                                                                        <div class="space-y-2">
                                                                            <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
                                                                                <h3 class="text-sm font-semibold text-gray-700 mb-2">ASR Latency Statistics</h3>
                                                                                <div class="grid grid-cols-3 gap-4">
                                                                                    <div>
                                                                                        <div class="text-xs text-gray-500">Average</div>
                                                                                        <div class="text-sm font-medium text-gray-900" x-text="test.avg_asr_latency_ms ? test.avg_asr_latency_ms + ' ms' : 'N/A'"></div>
                                                                                    </div>
                                                                                    <div>
                                                                                        <div class="text-xs text-gray-500">Min</div>
                                                                                        <div class="text-sm font-medium text-gray-900" x-text="test.min_asr_latency_ms ? test.min_asr_latency_ms + ' ms' : 'N/A'"></div>
                                                                                    </div>
                                                                                    <div>
                                                                                        <div class="text-xs text-gray-500">Max</div>
                                                                                        <div class="text-sm font-medium text-gray-900" x-text="test.max_asr_latency_ms ? test.max_asr_latency_ms + ' ms' : 'N/A'"></div>
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            
                                                            <div x-show="test.activeTab === 'system_prompt'">
                                                                <template x-if="test.system_prompt">
                                                                    <div class="my-2">
                                                                        <div class="ml-3 mt-2">
                                                                            <div class="bg-amber-50 border-l-4 border-amber-400 p-2 rounded">
                                                                                <div class="text-amber-900 text-sm whitespace-pre-wrap" x-text="test.system_prompt"></div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </template>
                                                                <template x-if="!test.system_prompt">
                                                                    <div class="mt-2 text-gray-500 text-xs italic">No system prompt available</div>
                                                                </template>
                                                            </div>
                                                            
                                                            <div x-show="test.activeTab === 'trace'">
                                                                <template x-if="test.trace_data">
                                                                    <div class="my-2 w-full max-w-full">
                                                                        <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 w-full">
                                                                            <h3 class="text-sm font-semibold text-gray-700 mb-4">Trace Timeline</h3>
                                                                            <div x-data="traceTimeline(test.trace_data)" x-init="initTimeline()" class="w-full">
                                                                                <!-- Timeline Container -->
                                                                                <div class="relative overflow-x-auto w-full min-w-0">
                                                                                    <!-- Timeline Header with Scale -->
                                                                                    <div class="flex mb-4 w-full min-w-[500px]">
                                                                                        <!-- Label space -->
                                                                                        <div class="w-64 flex-shrink-0 timeline-label-column"></div>
                                                                                        <!-- Scale -->
                                                                                        <div class="flex-1 relative h-6">
                                                                                            <div class="absolute inset-0 flex justify-between">
                                                                                                <template x-for="tick in timelineTicks" :key="tick.index">
                                                                                                    <div class="flex flex-col items-center">
                                                                                                        <div class="h-2 w-px bg-gray-300"></div>
                                                                                                        <div class="text-xs text-gray-500" x-text="tick.label"></div>
                                                                                                    </div>
                                                                                                </template>
                                                                                            </div>
                                                                                        </div>
                                                                                        <!-- Right padding -->
                                                                                        <div class="w-4 flex-shrink-0"></div>
                                                                                    </div>

                                                                                    <!-- Spans Container with Vertical Scroll -->
                                                                                    <div class="relative max-h-[500px] overflow-y-auto">
                                                                                        <div class="space-y-1 w-full min-w-[500px]">
                                                                                            <template x-for="span in sortedSpans" :key="span.span_id">
                                                                                                <div class="flex items-center h-8">
                                                                                                    <!-- Span Label -->
                                                                                                    <div class="w-64 pr-4 flex-shrink-0 flex items-center timeline-label-column">
                                                                                                        <div class="text-xs font-medium text-gray-700 truncate text-left w-full timeline-text" x-text="span.name"></div>
                                                                                                    </div>
                                                                                                    <!-- Span Timeline -->
                                                                                                    <div class="flex-1 relative flex items-center h-full">
                                                                                                        <!-- Span Bar -->
                                                                                                        <div class="absolute h-6 rounded cursor-pointer hover:opacity-80"
                                                                                                            :class="{
                                                                                                                'span-internal': span.kind === 'internal',
                                                                                                                'span-client': span.kind === 'client',
                                                                                                                'span-producer': span.kind === 'producer',
                                                                                                                'span-consumer': span.kind === 'consumer',
                                                                                                                'span-error': span.status === 'error'
                                                                                                            }"
                                                                                                            :style="getSpanStyle(span)"
                                                                                                            @click="toggleSpanDetails(span)">
                                                                                                            <span x-text="getSpanDuration(span) + 'ms'" 
                                                                                                                class="absolute flex items-center text-white font-medium whitespace-nowrap timeline-text"
                                                                                                                :class="{'duration-text': isSpanTooSmall(span), 'px-1 text-xs': !isSpanTooSmall(span)}">
                                                                                                            </span>
                                                                                                        </div>
                                                                                                    </div>
                                                                                                    <!-- Right padding -->
                                                                                                    <div class="w-4 flex-shrink-0"></div>
                                                                                                </div>
                                                                                            </template>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>

                                                                                <!-- Span Details Modal -->
                                                                                <div x-show="selectedSpan" 
                                                                                        x-transition
                                                                                        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
                                                                                        @click.self="selectedSpan = null">
                                                                                    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto" @click.stop>
                                                                                        <div class="p-4 border-b border-gray-200">
                                                                                            <div class="flex justify-between items-start">
                                                                                                <div>
                                                                                                    <h3 class="text-lg font-semibold text-gray-900" x-text="selectedSpan?.name"></h3>
                                                                                                    <p class="text-sm text-gray-500">
                                                                                                        Duration: <span x-text="getSpanDuration(selectedSpan) + 'ms'"></span>
                                                                                                    </p>
                                                                                                </div>
                                                                                                <button @click="selectedSpan = null" class="text-gray-400 hover:text-gray-500">
                                                                                                    <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                                                                                                        <path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"></path>
                                                                                                    </svg>
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div class="p-4 space-y-4">
                                                                                            <!-- Span Details -->
                                                                                            <div>
                                                                                                <h4 class="text-sm font-semibold text-gray-700 mb-2">Details</h4>
                                                                                                <div class="grid grid-cols-2 gap-2 text-xs">
                                                                                                    <div class="text-gray-500">Span ID:</div>
                                                                                                    <div class="font-mono break-all" x-text="selectedSpan?.span_id"></div>
                                                                                                    <div class="text-gray-500">Parent Span ID:</div>
                                                                                                    <div class="font-mono break-all" x-text="selectedSpan?.parent_span_id || 'None'"></div>
                                                                                                    <div class="text-gray-500">Kind:</div>
                                                                                                    <div class="capitalize" x-text="selectedSpan?.kind"></div>
                                                                                                    <div class="text-gray-500">Status:</div>
                                                                                                    <div class="capitalize" x-text="selectedSpan?.status"></div>
                                                                                                    <div class="text-gray-500">Start Time:</div>
                                                                                                    <div x-text="new Date(selectedSpan?.start_time).toLocaleString()"></div>
                                                                                                    <div class="text-gray-500">End Time:</div>
                                                                                                    <div x-text="selectedSpan?.end_time ? new Date(selectedSpan.end_time).toLocaleString() : 'Not ended'"></div>
                                                                                                </div>
                                                                                            </div>
                                                                                            
                                                                                            <!-- Attributes -->
                                                                                            <template x-if="Object.keys(selectedSpan?.attributes || {}).length > 0">
                                                                                                <div>
                                                                                                    <h4 class="text-sm font-semibold text-gray-700 mb-2">Attributes</h4>
                                                                                                    <div class="bg-gray-50 rounded p-2 overflow-x-auto">
                                                                                                        <pre class="text-xs whitespace-pre-wrap break-words max-w-full"><code x-text="JSON.stringify(selectedSpan.attributes, null, 2)"></code></pre>
                                                                                                    </div>
                                                                                                </div>
                                                                                            </template>
                                                                                            
                                                                                            <!-- Events -->
                                                                                            <template x-if="selectedSpan?.events?.length > 0">
                                                                                                <div>
                                                                                                    <h4 class="text-sm font-semibold text-gray-700 mb-2">Events</h4>
                                                                                                    <div class="space-y-2">
                                                                                                        <template x-for="event in selectedSpan.events" :key="event.timestamp">
                                                                                                            <div class="bg-gray-50 rounded p-2">
                                                                                                                <div class="flex justify-between text-xs">
                                                                                                                    <span class="font-medium" x-text="event.name"></span>
                                                                                                                    <span class="text-gray-500" x-text="new Date(event.timestamp).toLocaleString()"></span>
                                                                                                                </div>
                                                                                                                <template x-if="Object.keys(event.attributes || {}).length > 0">
                                                                                                                    <pre class="mt-1 text-xs whitespace-pre-wrap break-words max-w-full"><code x-text="JSON.stringify(event.attributes, null, 2)"></code></pre>
                                                                                                                </template>
                                                                                                            </div>
                                                                                                        </template>
                                                                                                    </div>
                                                                                                </div>
                                                                                            </template>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                                
                                                                                <!-- Legend -->
                                                                                <div class="mt-4 flex flex-wrap gap-4">
                                                                                    <div class="flex items-center">
                                                                                        <div class="w-3 h-3 span-internal rounded mr-2"></div>
                                                                                        <span class="text-xs text-gray-600 timeline-text">Internal</span>
                                                                                    </div>
                                                                                    <div class="flex items-center">
                                                                                        <div class="w-3 h-3 span-client rounded mr-2"></div>
                                                                                        <span class="text-xs text-gray-600 timeline-text">Client</span>
                                                                                    </div>
                                                                                    <div class="flex items-center">
                                                                                        <div class="w-3 h-3 span-producer rounded mr-2"></div>
                                                                                        <span class="text-xs text-gray-600 timeline-text">Producer</span>
                                                                                    </div>
                                                                                    <div class="flex items-center">
                                                                                        <div class="w-3 h-3 span-consumer rounded mr-2"></div>
                                                                                        <span class="text-xs text-gray-600 timeline-text">Consumer</span>
                                                                                    </div>
                                                                                    <div class="flex items-center">
                                                                                        <div class="w-3 h-3 span-error rounded mr-2"></div>
                                                                                        <span class="text-xs text-gray-600 timeline-text">Error</span>
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </template>
                                                                <template x-if="!test.trace_data">
                                                                    <div class="mt-2 text-gray-500 text-xs italic">No trace data available</div>
                                                                </template>
                                                            </div>
                                                        </div>
                                                        
                                                        <div>
                                                            <span class="font-semibold text-gray-800">Test Arguments:</span>
                                                                <div class="ml-3 mt-1 font-mono text-xs bg-gray-50 p-2 rounded border border-gray-100" x-text="test.test_arguments"></div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    </template>
                                </div>
                            </table>
                        </div>
                    </div>
                </template>
            </div>
        </template>
    </div>
    
    <script>
        function testResults() {
            return {
                tests: """
            + json.dumps(test_data)
            + """,
                groupBy: 'global_run_id',
                showFailing: false,
                searchTerm: '',
                startDate: '',
                endDate: '',
                searchInfoVisible: false,
                generatedDate: new Date().toLocaleString(),
                expandedGroups: {},
                expandedTests: {},
                
                get hasActiveFilters() {
                    return this.showFailing || this.searchTerm || this.startDate || this.endDate;
                },
                
                clearAllFilters() {
                    this.showFailing = false;
                    this.searchTerm = '';
                    this.startDate = '';
                    this.endDate = '';
                },
                
                clearDateFilters() {
                    this.startDate = '';
                    this.endDate = '';
                },
                
                filterToday() {
                    const today = new Date();
                    const year = today.getFullYear();
                    const month = String(today.getMonth() + 1).padStart(2, '0');
                    const day = String(today.getDate()).padStart(2, '0');
                    const formattedDate = `${year}-${month}-${day}`;
                    
                    this.startDate = formattedDate;
                    this.endDate = formattedDate;
                },
                
                isDateInRange(testDate) {
                    if (!testDate) return true;
                    if (!this.startDate && !this.endDate) return true;
                    
                    const date = new Date(testDate);
                    let start = this.startDate ? new Date(this.startDate) : null;
                    let end = this.endDate ? new Date(this.endDate) : null;
                    
                    // Set end date to end of day
                    if (end) {
                        end.setHours(23, 59, 59, 999);
                    }
                    
                    if (start && end) {
                        return date >= start && date <= end;
                    } else if (start) {
                        return date >= start;
                    } else if (end) {
                        return date <= end;
                    }
                    
                    return true;
                },
                
                get filteredTests() {
                    return this.tests.filter(test => {
                        // Filter by failing if option is selected
                        if (this.showFailing && test.success) {
                            return false;
                        }
                        
                        // Filter by date range
                        if (!this.isDateInRange(test.timestamp_original)) {
                            return false;
                        }
                        
                        // Filter by search term
                        if (this.searchTerm) {
                            const searchLower = this.searchTerm.toLowerCase();
                            const transcriptMatch = test.transcript && test.transcript.some(msg => 
                                msg.text.toLowerCase().includes(searchLower)
                            );
                            
                            return (
                                (test.test_name && test.test_name.toLowerCase().includes(searchLower)) ||
                                (test.global_run_id && test.global_run_id.toLowerCase().includes(searchLower)) ||
                                (test.run_id && test.run_id.toLowerCase().includes(searchLower)) ||
                                (test.error && test.error.toLowerCase().includes(searchLower)) ||
                                (test.assertions_details && test.assertions_details.toLowerCase().includes(searchLower)) ||
                                (test.system_prompt && test.system_prompt.toLowerCase().includes(searchLower)) ||
                                (test.is_ci && test.is_ci.toLowerCase().includes(searchLower)) ||
                                transcriptMatch
                            );
                        }
                        
                        return true;
                    }).map(test => {
                        // Ensure each test has a showDetails property
                        if (typeof test.showDetails === 'undefined') {
                            test.showDetails = false;
                        }
                        return test;
                    });
                },
                
                get groupedTests() {
                    const grouped = {};
                    
                    this.filteredTests.forEach(test => {
                        let groupKey;
                        if (this.groupBy === 'date') {
                            groupKey = test.date || 'Unknown Date';
                        } else if (this.groupBy === 'test_name') {
                            groupKey = test.test_name || 'Unknown Test';
                        } else {
                            // Default to global_run_id
                            groupKey = test.global_run_id || 'Unknown Run';
                        }
                        
                        if (!grouped[groupKey]) {
                            grouped[groupKey] = [];
                        }
                        
                        grouped[groupKey].push(test);
                    });
                    
                    // Sort groups by key
                    let sortedKeys = Object.keys(grouped);
                    
                    // For date grouping or global_run_id, sort in reverse chronological order (newest first)
                    if (this.groupBy === 'date' || this.groupBy === 'global_run_id') {
                        // For global_run_id, use the timestamp of the first test in each group for sorting
                        if (this.groupBy === 'global_run_id') {
                            sortedKeys.sort((a, b) => {
                                const timestampA = grouped[a][0]?.timestamp_original || '';
                                const timestampB = grouped[b][0]?.timestamp_original || '';
                                return timestampB.localeCompare(timestampA);
                            });
                        } else {
                            sortedKeys.sort().reverse();
                        }
                    } else {
                        sortedKeys.sort();
                    }
                    
                    return sortedKeys.reduce((obj, key) => {
                        obj[key] = grouped[key];
                        return obj;
                    }, {});
                },
                
                get passingCount() {
                    return this.filteredTests.filter(test => test.success).length;
                },
                
                get failingCount() {
                    return this.filteredTests.filter(test => !test.success).length;
                },
                
                countPassingInGroup(group) {
                    return group.filter(test => test.success).length;
                },
                
                countFailingInGroup(group) {
                    return group.filter(test => !test.success).length;
                },
                
                toggleGroup(groupName) {
                    this.expandedGroups[groupName] = !this.expandedGroups[groupName];
                },
                
                isTestExpanded(testId) {
                    return !!this.expandedTests[testId];
                },
                
                toggleTestDetails(testId) {
                    this.expandedTests[testId] = !this.expandedTests[testId];
                },
                
                formatAssertions(assertionsText) {
                    if (!assertionsText) return '';
                    
                    // Replace newlines with <br> tags
                    let formatted = assertionsText.replace(/\\n/g, '<br>');
                    
                    // Highlight PASSED/FAILED
                    formatted = formatted.replace(/\(PASSED\)/g, '<span class="text-blue-600 font-semibold">(PASSED)</span>');
                    formatted = formatted.replace(/\(FAILED\)/g, '<span class="text-red-600 font-semibold">(FAILED)</span>');
                    
                    return formatted;
                },
                
                collapseAllInGroup(group) {
                    // Hide all detail rows in this group
                    for (const test of group) {
                        if (this.isTestExpanded(test.run_id)) {
                            // Set the expanded state to false
                            this.expandedTests[test.run_id] = false;
                            
                            // Hide the details row
                            const detailsRow = document.getElementById('details-' + test.run_id);
                            if (detailsRow) {
                                detailsRow.style.display = 'none';
                            }
                        }
                    }
                },
                
                collapseAll() {
                    // Reset all expanded tests
                    this.expandedTests = {};
                    
                    // Collapse all groups
                    for (const groupName in this.expandedGroups) {
                        this.expandedGroups[groupName] = false;
                    }
                    
                    // Hide all detail rows
                    const detailRows = document.querySelectorAll('[id^="details-"]');
                    detailRows.forEach(row => {
                        row.style.display = 'none';
                    });
                },
                
                getGroupLatencyStats(group) {
                    const latencies = group.reduce((acc, test) => {
                        if (test.avg_asr_latency_ms) {
                            acc.push(parseFloat(test.avg_asr_latency_ms));
                        }
                        return acc;
                    }, []);
                    
                    if (latencies.length === 0) {
                        return { avg: null, min: null, max: null };
                    }
                    
                    return {
                        avg: latencies.reduce((a, b) => a + b, 0) / latencies.length,
                        min: Math.min(...latencies),
                        max: Math.max(...latencies)
                    };
                },
                
                isSpanTooSmall(span) {
                    if (!span || !span._normalized) return false;
                    // If span width is less than 5% of timeline, show duration outside
                    return (span._normalized.end - span._normalized.start) < 0.05;
                },
                
                traceTimeline(traceData) {
                    return {
                        trace: JSON.parse(traceData),
                        timelineTicks: [],
                        selectedSpan: null,
                        sortedSpans: [],
                        
                        initTimeline() {
                            try {
                                const spans = this.trace.spans || [];
                                if (spans.length === 0) return;
                                
                                // Calculate timeline range
                                let minTime = Infinity;
                                let maxTime = -Infinity;
                                
                                spans.forEach(span => {
                                    const startTime = new Date(span.start_time).getTime();
                                    const endTime = span.end_time ? new Date(span.end_time).getTime() : startTime;
                                    minTime = Math.min(minTime, startTime);
                                    maxTime = Math.max(maxTime, endTime);
                                });
                                
                                // Store timeline data
                                this.timelineStart = minTime;
                                this.timelineDuration = maxTime - minTime;
                                
                                // Create evenly spaced ticks
                                const tickCount = 10;
                                this.timelineTicks = Array.from({ length: tickCount + 1 }, (_, i) => {
                                    return {
                                        index: i,
                                        label: Math.round((this.timelineDuration / tickCount) * i) + 'ms'
                                    };
                                });
                                
                                // Process spans
                                this.processSpans(spans);
                            } catch (error) {
                                console.error("Error initializing timeline:", error);
                            }
                        },
                        
                        processSpans(spans) {
                            // Create a map of spans by their ID
                            const spanMap = new Map(spans.map(span => [span.span_id, span]));
                            
                            // Helper function to get span depth
                            const getSpanDepth = (span) => {
                                let depth = 0;
                                let current = span;
                                while (current.parent_span_id && spanMap.has(current.parent_span_id)) {
                                    depth++;
                                    current = spanMap.get(current.parent_span_id);
                                }
                                return depth;
                            };
                            
                            // Sort spans by depth (parent-child relationships) and then by start time
                            this.sortedSpans = [...spans].sort((a, b) => {
                                const depthA = getSpanDepth(a);
                                const depthB = getSpanDepth(b);
                                if (depthA !== depthB) return depthA - depthB;
                                return new Date(a.start_time) - new Date(b.start_time);
                            });
                            
                            // Calculate normalized positions for each span
                            this.sortedSpans.forEach(span => {
                                const startTime = new Date(span.start_time).getTime();
                                const endTime = span.end_time ? new Date(span.end_time).getTime() : startTime;
                                
                                span._normalized = {
                                    start: (startTime - this.timelineStart) / this.timelineDuration,
                                    end: (endTime - this.timelineStart) / this.timelineDuration,
                                    duration: endTime - startTime
                                };
                            });
                        },
                        
                        getSpanStyle(span) {
                            if (!span._normalized) return '';
                            
                            const left = (span._normalized.start * 100) + '%';
                            const width = Math.max((span._normalized.end - span._normalized.start) * 100, 0.5) + '%';
                            
                            return `left: ${left}; width: ${width};`;
                        },
                        
                        getSpanDuration(span) {
                            if (!span || !span._normalized) return 0;
                            return Math.round(span._normalized.duration);
                        },
                        
                        toggleSpanDetails(span) {
                            this.selectedSpan = this.selectedSpan?.span_id === span.span_id ? null : span;
                        }
                    };
                }
            };
        }
    </script>
</body>
</html>"""
        )

    console.print(f"[green]HTML report generated at: [bold]{output_path}[/bold]")
    return output_path
