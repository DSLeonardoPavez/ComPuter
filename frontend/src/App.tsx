import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Header from './components/Header';
import Footer from './components/Footer';
import ChatBot from './components/ChatBot/ChatBot';
import HomePage from './pages/HomePage';
import ComponentSearch from './pages/ComponentSearch';
import ComparisonTool from './pages/ComparisonTool';
import RecommendationTool from './pages/RecommendationTool';
import UserProfileWizard from './pages/UserProfileWizard';
import AdminPanel from './pages/AdminPanel';
import './App.css';

// Crear tema personalizado
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 500,
    },
  },
});

function App() {
  const [chatOpen, setChatOpen] = useState(false);

  const handleToggleChat = () => {
    setChatOpen(!chatOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<ComponentSearch />} />
            <Route path="/recommendations" element={<RecommendationTool />} />
            <Route path="/comparison" element={<ComparisonTool />} />
            <Route path="/profile" element={<UserProfileWizard />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </main>
        <Footer />
        <ChatBot isOpen={chatOpen} onToggle={handleToggleChat} />
      </div>
    </ThemeProvider>
  );
}

export default App;