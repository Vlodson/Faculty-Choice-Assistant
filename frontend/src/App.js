import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

function Header() {
  return (
    <Box sx={{ textAlign: 'center', marginTop: 4 }}>
      <Typography variant="h3">Faculty Choice Assistant</Typography>
    </Box>
  );
}

function ChatBox({ onSendMessage }) {
  const [message, setMessage] = useState('');

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <Box sx={{ margin: '4rem 20% 4rem', textAlign: 'center', bottom: 0 }}>
      <TextField
        label="What can I help you with?"
        variant="outlined"
        fullWidth
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        sx={{
          '& label.Mui-focused': { textAlign: 'center' },
          '& .MuiInputBase-input': { textAlign: 'center' },
          '& .MuiOutlinedInput-root': { borderRadius: 8 },
        }}
      />
    </Box>
  );
}

function ResultsBox({ content }) {
  const containerRef = useRef(null);

  useEffect(() => {
    // Scroll to the bottom when content changes
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [content]);

  return (
    <Box
      ref={containerRef}
      sx={{
        margin: '2rem 20%',
        padding: '1rem',
        borderRadius: 8,
        border: '1px solid #ccc',
        overflowY: 'auto',
        maxHeight: '80%',
        whiteSpace: 'pre',
      }}
    >
      {content}
    </Box>
  );
}

function PredefinedQueriesBox({ onQuerySelect }) {
  return (
    <Box
      sx={{
        backgroundColor: '#5eeb7c',
        padding: '1rem',
        width: '20%',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <Typography variant="h6" sx={{ color: '#fff', marginBottom: '1rem' }}>
        Predefined Queries
      </Typography>
      <Button
        variant="contained"
        onClick={() => onQuerySelect('Universities')}
        sx={{ width: '100%', marginBottom: '0.5rem' }}
      >
        Universities
      </Button>
      <Button
        variant="contained"
        onClick={() => onQuerySelect('Faculties in Novi Sad')}
        sx={{ width: '100%', marginBottom: '0.5rem' }}
      >
        Faculties in Novi Sad
      </Button>
      <Button
        variant="contained"
        onClick={() => onQuerySelect('FTN NS knowledge areas')}
        sx={{ width: '100%' }}
      >
        FTN NS Knowledge Areas
      </Button>
    </Box>
  );
}

function App() {
  const [threadId, setThreadId] = useState(null);
  const [runId, setRunId] = useState(null);
  const [chatContent, setChatContent] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5001/chat/setup');
        const { thread_id, run_id } = response.data;

        // Set the retrieved values in state
        setThreadId(thread_id);
        setRunId(run_id);

        setChatContent("Assistant: Your chat has been succesfully set up!")
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const addChatContent = (newContent) => {
    setChatContent((prevContent) => [...prevContent, '\n\n', newContent]);
  };

  const sendMessage = async (msg) => {
    try {
      const response = await axios.post('http://localhost:5001/chat/message', {
        thread_id: threadId,
        run_id: runId,
        msg,
      });

      const { thread_id: newThreadId, run_id: newRunId } = response.data;

      // Set the new values in state
      setThreadId(newThreadId);
      setRunId(newRunId);

      // Add the sent message to the chat
      addChatContent(`You: ${msg}`);

      // Fetch query results after sending the message
      const queryResultsResponse = await axios.get('http://localhost:5001/chat/query_results', {
        params: {
          thread_id: newThreadId,
          run_id: newRunId,
        },
      });
      console.log(queryResultsResponse);

      // Process the query results as needed
      const queryResults = queryResultsResponse.data;

      const columns = Object.keys(queryResults);
      const rows = queryResults[columns[0]].map((_, rowIndex) =>
        columns.reduce((row, column) => {
          row[column] = queryResults[column][rowIndex];
          return row;
        }, {})
      );

      // Display the formatted table
      addChatContent("Assistant:\n" + formatTable(columns, rows));

    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const formatTable = (columns, rows) => {
    const columnWidths = {};

    // Find the maximum width for each column
    columns.forEach((column) => {
      const maxWidth = Math.max(
        ...rows.map((row) => (row[column] ? String(row[column]).length : 0))
      );
      columnWidths[column] = maxWidth;
    });

    const table = [];

    // Format header
    table.push(
      columns.map((column) => column.padEnd(columnWidths[column], ' ')).join('\t| ')
    );

    table.push(
      columns
        .map((column) => '-'.repeat(columnWidths[column]))
        .join('\t')
    );

    // Format rows
    rows.forEach((row) => {
      table.push(
        columns
          .map((column) =>
            String(row[column]).padEnd(columnWidths[column], ' ')
          )
          .join('\t| ')
      );
    });

    return table.join('\n');
  };


  const handlePredefinedQuerySelect = async (query) => {
    try {
      addChatContent("You: Predefined Query - " + query)
      // Make the predefined query request to the updated endpoint
      const response = await axios.get('http://localhost:5001/predef_queries/', {
        params: {
          query: query,
        },
      });

      const predefinedQueryResults = response.data;

      const columns = Object.keys(predefinedQueryResults);
      const rows = predefinedQueryResults[columns[0]].map((_, rowIndex) =>
        columns.reduce((row, column) => {
          row[column] = predefinedQueryResults[column][rowIndex];
          return row;
        }, {})
      );

      addChatContent(formatTable(columns, rows));
    } catch (error) {
      console.error('Error fetching predefined query results:', error);
    }
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <PredefinedQueriesBox onQuerySelect={handlePredefinedQuerySelect} />
      <div style={{ flex: 1 }}>
        <Header />
        <ResultsBox content={chatContent} />
        <ChatBox onSendMessage={sendMessage} />
      </div>
    </Box>
  );
}

export default App;
