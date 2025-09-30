import axios from 'axios';
import { API_URL } from './api';

export interface IChatMessage {
  role: string;
  content: string;
  timestamp?: string;
}

export interface IChatRequest {
  message: string;
  session_id?: string;
}

export interface IChatResponse {
  message: string;
  session_id: string;
}

export interface IChatHistoryResponse {
  messages: IChatMessage[];
  session_id: string;
}

const chatService = {
  sendMessage: async (message: string, sessionId?: string): Promise<IChatResponse> => {
    const response = await axios.post(`${API_URL}/api/chatbot/chat`, {
      message,
      session_id: sessionId
    });
    return response.data;
  },

  getChatHistory: async (sessionId: string): Promise<IChatHistoryResponse> => {
    const response = await axios.get(`${API_URL}/api/chatbot/history/${sessionId}`);
    return response.data;
  },

  deleteChatHistory: async (sessionId: string): Promise<void> => {
    await axios.delete(`${API_URL}/api/chatbot/history/${sessionId}`);
  }
};

export default chatService;