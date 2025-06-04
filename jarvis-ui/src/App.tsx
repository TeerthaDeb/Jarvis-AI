import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import theme from './theme';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <ChatInterface />
    </ChakraProvider>
  );
}

export default App; 