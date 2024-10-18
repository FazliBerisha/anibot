import React, { useState, useEffect, useRef } from 'react';
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import { TextField, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';

const theme = {
  primary: '#8A2BE2',
  secondary: '#E6E6FA',
  background: '#F8F8FF',
  text: '#4B0082',
};

const GlobalStyle = createGlobalStyle`
  body {
    background-color: ${props => props.theme.background};
    font-family: 'Comic Sans MS', cursive, sans-serif;
  }
`;

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 20px;
`;

const Title = styled.h1`
  color: ${props => props.theme.primary};
  font-size: 3em;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
`;

const Subtitle = styled.p`
  color: ${props => props.theme.text};
  font-size: 1.2em;
`;

const ChatContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: ${props => props.theme.secondary};
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Message = styled.div`
  margin-bottom: 15px;
  padding: 10px 15px;
  border-radius: 20px;
  max-width: 80%;
  animation: pop-in 0.3s ease-out;

  @keyframes pop-in {
    0% { transform: scale(0.8); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
  }
`;

const BotMessage = styled(Message)`
  background-color: ${props => props.theme.primary};
  color: white;
  align-self: flex-start;
  border-bottom-left-radius: 0;
`;

const UserMessage = styled(Message)`
  background-color: white;
  color: ${props => props.theme.text};
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 0;
`;

const InputContainer = styled.div`
  display: flex;
  align-items: center;
  margin-top: 20px;
`;

const StyledTextField = styled(TextField)`
  .MuiOutlinedInput-root {
    border-radius: 30px;
    background-color: white;
  }
`;

const StyledIconButton = styled(IconButton)`
  background-color: ${props => props.theme.primary} !important;
  color: white !important;
  margin-left: 10px !important;
  padding: 10px !important;
  transition: transform 0.2s !important;

  &:hover {
    transform: scale(1.1);
  }
`;

function useChatbot() {
  const [messages, setMessages] = useState([
    { sender: 'AniBot', text: 'Hello! I\'m AniBot, your anime companion. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const addMessage = (sender, text) => {
    setMessages(prev => [...prev, { sender, text }]);
  };

  const handleSend = async () => {
    if (input.trim()) {
      addMessage('User', input);
      setInput('');
      setIsTyping(true);

      try {
        const response = await axios.post('http://localhost:8000/api/v1/chat/', { message: input });
        setIsTyping(false);
        addMessage('AniBot', response.data.response);
      } catch (error) {
        console.error('Error:', error);
        setIsTyping(false);
        addMessage('System', 'Error: Unable to connect to the server. Please try again later.');
      }
    }
  };

  return { messages, input, isTyping, setInput, handleSend };
}

function App() {
  const { messages, input, isTyping, setInput, handleSend } = useChatbot();
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <AppContainer>
        <Header>
          <Title>AniBot</Title>
          <Subtitle>Your Bubbly Anime Companion</Subtitle>
        </Header>
        <ChatContainer ref={chatContainerRef}>
          {messages.map((message, index) => (
            message.sender === 'AniBot' ? (
              <BotMessage key={index}>{message.text}</BotMessage>
            ) : (
              <UserMessage key={index}>{message.text}</UserMessage>
            )
          ))}
          {isTyping && <BotMessage>AniBot is typing...</BotMessage>}
        </ChatContainer>
        <InputContainer>
          <StyledTextField
            fullWidth
            variant="outlined"
            placeholder="Ask me about anime..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <StyledIconButton onClick={handleSend}>
            <SendIcon />
          </StyledIconButton>
        </InputContainer>
      </AppContainer>
    </ThemeProvider>
  );
}

export default App;
