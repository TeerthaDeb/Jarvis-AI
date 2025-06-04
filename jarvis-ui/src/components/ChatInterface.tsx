import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  VStack,
  Input,
  IconButton,
  Flex,
  Container,
  useColorMode,
  Switch,
  FormControl,
  FormLabel,
  HStack,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  Button,
  FormErrorMessage,
  useToast,
} from '@chakra-ui/react';
import { FaMicrophone, FaStop } from 'react-icons/fa';
import axios from 'axios';
import ChatMessage from './ChatMessage';
import ArcReactor from './ArcReactor';

interface Message {
  text: string;
  isUser: boolean;
  timestamp: Date;
  videoId?: string;
}

interface UserData {
  name: string;
  pronunciation: string;
  birth_date: string;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeechMode, setIsSpeechMode] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isSetupModalOpen, setIsSetupModalOpen] = useState(false);
  const [isSetupComplete, setIsSetupComplete] = useState(false);
  const [setupForm, setSetupForm] = useState<UserData>({
    name: '',
    pronunciation: '',
    birth_date: '',
  });
  const [setupErrors, setSetupErrors] = useState<Partial<UserData>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const { colorMode } = useColorMode();
  const toast = useToast();
  const bgColor = colorMode === 'light' ? 'gray.50' : 'gray.900';
  const inputBgColor = colorMode === 'light' ? 'white' : 'gray.700';


  useEffect(() => {
    const checkUserStatus = async () => {
      try {
        const { data } = await axios.get('http://localhost:5000/user/status');
        if (data.status === 'setup_complete') {
          setIsSetupComplete(true);
          // Add initial greeting message
          const greetingMessage: Message = {
            text: data.user.greeting || "Hello! I am Jarvis, your AI assistant.",
            isUser: false,
            timestamp: new Date(),
          };
          setMessages([greetingMessage]);
        } else {
          setIsSetupModalOpen(true);
        }
      } catch (error) {
        console.error('Error checking user status:', error);
        toast({
          title: 'Error',
          description: 'Failed to check user status. Please try again.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    };

    checkUserStatus();
  }, [toast]);

  const handleSetupSubmit = async () => {
    // Validate form
    const errors: Partial<UserData> = {};
    if (!setupForm.name) errors.name = 'Name is required';
    if (!setupForm.pronunciation) errors.pronunciation = 'Pronunciation is required';
    if (!setupForm.birth_date) errors.birth_date = 'Birth date is required';
    
    if (Object.keys(errors).length > 0) {
      setSetupErrors(errors);
      return;
    }

    try {
      const { data } = await axios.post('http://localhost:5000/user/setup', setupForm);
      setIsSetupComplete(true);
      setIsSetupModalOpen(false);
      
      // Add welcome message
      const welcomeMessage: Message = {
        text: `Welcome ${data.user.name}! I am Jarvis, your AI assistant. How may I help you?`,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);

      toast({
        title: 'Setup Complete',
        description: 'User setup completed successfully!',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error during setup:', error);
      toast({
        title: 'Setup Failed',
        description: 'Failed to complete user setup. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  useEffect(() => {
    scrollToBottom();
    // Initialize speech synthesis
    synthRef.current = window.speechSynthesis;
    
    // Cleanup on unmount
    return () => {
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const speakText = (text: string) => {
    if (!synthRef.current || !isSpeechMode) return;

    // Cancel any ongoing speech
    synthRef.current.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Configure voice settings
    utterance.rate = 1.0;  // Speed
    utterance.pitch = 1.0; // Pitch
    utterance.volume = 1.0; // Volume

    // Try to find a good voice
    const voices = synthRef.current.getVoices();
    const preferredVoice = voices.find(voice => 
      voice.name.includes('Google') || 
      voice.name.includes('Microsoft') || 
      voice.name.includes('Samantha')
    );
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    // Handle speech events
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    // Speak the text
    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
      setIsSpeaking(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !isSetupComplete) return;

    const newUserMessage: Message = {
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setInputMessage('');
    setIsThinking(true);
    scrollToBottom();

    try {
      // Create a temporary message for streaming
      const tempMessage: Message = {
        text: '',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, tempMessage]);

      const response = await fetch("http://localhost:5000/chat", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: inputMessage,
          speech_mode: isSpeechMode,
          stream: true
        })
      });

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      let fullResponse = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Convert the chunk to text
        const chunk = new TextDecoder().decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.token) {
                fullResponse += data.token;
                // Update the last message with the accumulated response
                setMessages((prev) => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = {
                    ...newMessages[newMessages.length - 1],
                    text: fullResponse
                  };
                  return newMessages;
                });
                scrollToBottom();
              }
              if (data.done) {
                if (isSpeechMode) {
                  speakText(fullResponse);
                }
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }
    } catch (e) {
      const errorMsg = (e instanceof Error) ? e.message : "Error communicating with backend";
      const newBackendMessage: Message = {
        text: "Error: " + errorMsg,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, newBackendMessage]);
      scrollToBottom();
    } finally {
      setIsThinking(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleListening = () => {
    setIsListening(!isListening);
    // TODO: Implement voice input functionality
  };

  return (
    <Container maxW="container.xl" h="100vh" position="relative" p={4}>
      {/* Setup Modal */}
      <Modal isOpen={isSetupModalOpen} onClose={() => {}} closeOnOverlayClick={false}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Welcome to Jarvis AI</ModalHeader>
          <ModalCloseButton isDisabled />
          <ModalBody pb={6}>
            <VStack spacing={4}>
              <FormControl isInvalid={!!setupErrors.name}>
                <FormLabel>Name</FormLabel>
                <Input
                  value={setupForm.name}
                  onChange={(e) => setSetupForm(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Enter your name"
                />
                <FormErrorMessage>{setupErrors.name}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!setupErrors.pronunciation}>
                <FormLabel>How to pronounce your name</FormLabel>
                <Input
                  value={setupForm.pronunciation}
                  onChange={(e) => setSetupForm(prev => ({ ...prev, pronunciation: e.target.value }))}
                  placeholder="e.g., John or Mr. Smith"
                />
                <FormErrorMessage>{setupErrors.pronunciation}</FormErrorMessage>
              </FormControl>

              <FormControl isInvalid={!!setupErrors.birth_date}>
                <FormLabel>Birth Date</FormLabel>
                <Input
                  type="date"
                  value={setupForm.birth_date}
                  onChange={(e) => setSetupForm(prev => ({ ...prev, birth_date: e.target.value }))}
                />
                <FormErrorMessage>{setupErrors.birth_date}</FormErrorMessage>
              </FormControl>

              <Button colorScheme="blue" onClick={handleSetupSubmit} width="full">
                Complete Setup
              </Button>
            </VStack>
          </ModalBody>
        </ModalContent>
      </Modal>

      {/* Arc Reactor Status - Fixed at top */}
      <Box 
        position="fixed" 
        top="10%" 
        left="50%" 
        transform="translateX(-50%)"
        w="full" 
        h="100px" 
        display="flex" 
        justifyContent="center" 
        alignItems="center"
        zIndex={1}
      >
        <ArcReactor isThinking={isThinking} />
      </Box>

      {/* Chat Messages - Scrollable */}
      <Box
        position="fixed"
        top="30%"
        left="50%"
        transform="translateX(-50%)"
        w="90%"
        h="60vh"
        overflowY="auto"
        borderRadius="lg"
        p={4}
        boxShadow="inner"
        zIndex={1}
      >
        <VStack spacing={4} align="stretch">
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message.text}
              isUser={message.isUser}
              timestamp={message.timestamp}
              onSpeak={isSpeechMode ? speakText : undefined}
              videoId={message.videoId}
              isThinking={!message.isUser && index === messages.length - 1 && isThinking}
            />
          ))}
          <div ref={messagesEndRef} />
        </VStack>
      </Box>

      {/* Input Area - Fixed at bottom */}
      <Flex 
        w="90%" 
        gap={2} 
        position="fixed" 
        bottom="2%" 
        left="50%" 
        transform="translateX(-50%)" 
        px={4} 
        direction="column" 
        align="center"
        zIndex={1}
      >
        <HStack spacing={4} mb={2}>
          <FormControl display="flex" alignItems="center">
            <FormLabel htmlFor="speech-mode" mb="0" fontSize="sm" color={colorMode === 'light' ? 'gray.600' : 'gray.300'}>
              {isSpeechMode ? 'Speech Mode' : 'Text Mode'}
            </FormLabel>
            <Switch
              id="speech-mode"
              isChecked={isSpeechMode}
              onChange={(e) => {
                setIsSpeechMode(e.target.checked);
                if (!e.target.checked) {
                  stopSpeaking();
                }
              }}
              colorScheme="blue"
              size="md"
            />
          </FormControl>
        </HStack>
        <Flex w="full" gap={2}>
          <Input
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isSetupComplete ? "Type your message..." : "Please complete setup first"}
            bg={inputBgColor}
            borderRadius="full"
            px={4}
            py={2}
            isDisabled={!isSetupComplete}
          />
          <IconButton
            aria-label={isListening ? 'Stop listening' : 'Start listening'}
            icon={isListening ? <FaStop /> : <FaMicrophone />}
            colorScheme={isListening ? 'red' : 'blue'}
            borderRadius="full"
            onClick={toggleListening}
            isDisabled={!isSetupComplete}
          />
        </Flex>
      </Flex>
    </Container>
  );
};

export default ChatInterface; 