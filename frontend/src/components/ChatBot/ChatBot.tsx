import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  Chip,
  Fab,
  Slide,
  Divider,
  CircularProgress,
  Tooltip,
  Stack,
  Card,
  CardContent,
  Button
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Close as CloseIcon,
  Chat as ChatIcon,
  Refresh as RefreshIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  ContentCopy as CopyIcon
} from '@mui/icons-material';
import chatService from '../../services/chatService';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  type?: 'text' | 'recommendation' | 'error';
  data?: any;
}

interface ChatBotProps {
  isOpen?: boolean;
  onToggle?: () => void;
}

const ChatBot: React.FC<ChatBotProps> = ({ isOpen = false, onToggle }) => {
  const [chatOpen, setChatOpen] = useState(isOpen);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '¡Hola! Soy tu asistente de ComPuter. Puedo ayudarte a encontrar componentes, verificar compatibilidad y responder preguntas sobre PCs. ¿En qué puedo ayudarte hoy?',
      sender: 'bot',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const handleToggleChat = () => {
    setChatOpen(!chatOpen);
    if (onToggle) {
      onToggle();
    }
  };
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await chatService.sendMessage(inputMessage);
      
      setTimeout(() => {
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: response.message,
          sender: 'bot',
          timestamp: new Date(),
          type: 'text'
        };

        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
        setIsTyping(false);
      }, 1000); // Simular tiempo de escritura
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, inténtalo de nuevo.',
        sender: 'bot',
        timestamp: new Date(),
        type: 'error'
      };

      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: '1',
        text: '¡Hola! Soy tu asistente de ComPuter. ¿En qué puedo ayudarte hoy?',
        sender: 'bot',
        timestamp: new Date(),
        type: 'text'
      }
    ]);
  };

  const handleCopyMessage = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const renderMessage = (message: Message) => {
    const isBot = message.sender === 'bot';
    
    return (
      <Box
        key={message.id}
        sx={{
          display: 'flex',
          justifyContent: isBot ? 'flex-start' : 'flex-end',
          mb: 2,
          alignItems: 'flex-start'
        }}
      >
        {isBot && (
          <Avatar
            sx={{
              bgcolor: 'primary.main',
              width: 32,
              height: 32,
              mr: 1,
              mt: 0.5
            }}
          >
            <BotIcon sx={{ fontSize: 18 }} />
          </Avatar>
        )}
        
        <Box sx={{ maxWidth: '75%' }}>
          <Paper
            elevation={1}
            sx={{
              p: 2,
              bgcolor: isBot ? 'grey.100' : 'primary.main',
              color: isBot ? 'text.primary' : 'white',
              borderRadius: isBot ? '16px 16px 16px 4px' : '16px 16px 4px 16px',
              position: 'relative',
              '&:hover .message-actions': {
                opacity: 1
              }
            }}
          >
            <Typography variant="body1" sx={{ wordBreak: 'break-word' }}>
              {message.text}
            </Typography>
            
            {message.type === 'recommendation' && message.data && (
              <Card sx={{ mt: 2, bgcolor: 'background.paper' }}>
                <CardContent sx={{ p: 2 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    Recomendación:
                  </Typography>
                  <Typography variant="body2">
                    {message.data.component_name} - ${message.data.price}
                  </Typography>
                  <Button size="small" sx={{ mt: 1 }}>
                    Ver detalles
                  </Button>
                </CardContent>
              </Card>
            )}
            
            <Box
              className="message-actions"
              sx={{
                position: 'absolute',
                top: -8,
                right: isBot ? -40 : 8,
                opacity: 0,
                transition: 'opacity 0.2s',
                display: 'flex',
                gap: 0.5
              }}
            >
              <Tooltip title="Copiar mensaje">
                <IconButton
                  size="small"
                  onClick={() => handleCopyMessage(message.text)}
                  sx={{
                    bgcolor: 'background.paper',
                    boxShadow: 1,
                    '&:hover': { bgcolor: 'grey.100' }
                  }}
                >
                  <CopyIcon sx={{ fontSize: 14 }} />
                </IconButton>
              </Tooltip>
              
              {isBot && (
                <>
                  <Tooltip title="Útil">
                    <IconButton
                      size="small"
                      sx={{
                        bgcolor: 'background.paper',
                        boxShadow: 1,
                        '&:hover': { bgcolor: 'success.light', color: 'white' }
                      }}
                    >
                      <ThumbUpIcon sx={{ fontSize: 14 }} />
                    </IconButton>
                  </Tooltip>
                  
                  <Tooltip title="No útil">
                    <IconButton
                      size="small"
                      sx={{
                        bgcolor: 'background.paper',
                        boxShadow: 1,
                        '&:hover': { bgcolor: 'error.light', color: 'white' }
                      }}
                    >
                      <ThumbDownIcon sx={{ fontSize: 14 }} />
                    </IconButton>
                  </Tooltip>
                </>
              )}
            </Box>
          </Paper>
          
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{
              display: 'block',
              textAlign: isBot ? 'left' : 'right',
              mt: 0.5,
              ml: isBot ? 1 : 0,
              mr: isBot ? 0 : 1
            }}
          >
            {formatTimestamp(message.timestamp)}
          </Typography>
        </Box>
        
        {!isBot && (
          <Avatar
            sx={{
              bgcolor: 'secondary.main',
              width: 32,
              height: 32,
              ml: 1,
              mt: 0.5
            }}
          >
            <PersonIcon sx={{ fontSize: 18 }} />
          </Avatar>
        )}
      </Box>
    );
  };

  const renderTypingIndicator = () => (
    <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
      <Avatar
        sx={{
          bgcolor: 'primary.main',
          width: 32,
          height: 32,
          mr: 1,
          mt: 0.5
        }}
      >
        <BotIcon sx={{ fontSize: 18 }} />
      </Avatar>
      
      <Paper
        elevation={1}
        sx={{
          p: 2,
          bgcolor: 'grey.100',
          borderRadius: '16px 16px 16px 4px',
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}
      >
        <CircularProgress size={16} />
        <Typography variant="body2" color="text.secondary">
          Escribiendo...
        </Typography>
      </Paper>
    </Box>
  );

  const quickActions = [
    '¿Qué CPU recomiendas para gaming?',
    'Verificar compatibilidad',
    'Presupuesto de $1000',
    'Componentes populares'
  ];

  if (!isOpen) {
    return (
      <Fab
        color="primary"
        onClick={onToggle}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          zIndex: 1000,
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
        }}
      >
        <ChatIcon />
      </Fab>
    );
  }

  return (
    <Box>
      <Slide direction="up" in={isOpen} mountOnEnter unmountOnExit>
        <Paper
          elevation={8}
          sx={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            width: { xs: 'calc(100vw - 32px)', sm: 400 },
            height: { xs: 'calc(100vh - 100px)', sm: 600 },
            zIndex: 1000,
            display: 'flex',
            flexDirection: 'column',
            borderRadius: 3,
            overflow: 'hidden'
          }}
        >
        {/* Header */}
        <Box
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            p: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Avatar sx={{ bgcolor: 'primary.dark', width: 32, height: 32 }}>
              <BotIcon sx={{ fontSize: 18 }} />
            </Avatar>
            <Box>
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                ComPuter Assistant
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                {isTyping ? 'Escribiendo...' : 'En línea'}
              </Typography>
            </Box>
          </Box>
          
          <Box>
            <Tooltip title="Limpiar chat">
              <IconButton
                size="small"
                onClick={handleClearChat}
                sx={{ color: 'white', mr: 1 }}
              >
                <RefreshIcon />
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Cerrar chat">
              <IconButton
                size="small"
                onClick={onToggle}
                sx={{ color: 'white' }}
              >
                <CloseIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {/* Messages */}
        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            p: 2,
            bgcolor: 'background.default'
          }}
        >
          {messages.map(renderMessage)}
          {isTyping && renderTypingIndicator()}
          <div ref={messagesEndRef} />
        </Box>

        {/* Quick Actions */}
        {messages.length === 1 && (
          <>
            <Divider />
            <Box sx={{ p: 2 }}>
              <Typography variant="caption" color="text.secondary" gutterBottom>
                Acciones rápidas:
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                {quickActions.map((action, index) => (
                  <Chip
                    key={index}
                    label={action}
                    size="small"
                    onClick={() => setInputMessage(action)}
                    sx={{
                      cursor: 'pointer',
                      '&:hover': { bgcolor: 'primary.light', color: 'white' }
                    }}
                  />
                ))}
              </Stack>
            </Box>
          </>
        )}

        {/* Input */}
        <Divider />
        <Box sx={{ p: 2, bgcolor: 'background.paper' }}>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
            <TextField
              ref={inputRef}
              fullWidth
              multiline
              maxRows={3}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu mensaje..."
              disabled={isLoading}
              variant="outlined"
              size="small"
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3
                }
              }}
            />
            
            <IconButton
              color="primary"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              sx={{
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': { bgcolor: 'primary.dark' },
                '&:disabled': { bgcolor: 'grey.300' }
              }}
            >
              {isLoading ? (
                <CircularProgress size={20} color="inherit" />
              ) : (
                <SendIcon />
              )}
            </IconButton>
          </Box>
          
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ display: 'block', textAlign: 'center', mt: 1 }}
          >
            Presiona Enter para enviar • Shift+Enter para nueva línea
          </Typography>
        </Box>
        </Paper>
      </Slide>
    </Box>
  );
};

export default ChatBot;