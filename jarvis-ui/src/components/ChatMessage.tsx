import * as React from 'react';
import { useState } from 'react';
import {
  Box,
  Text,
  Flex,
  IconButton,
  useColorMode,
  VStack,
} from '@chakra-ui/react';
import { FaUser, FaVolumeUp } from 'react-icons/fa';
import YouTubePlayer from './YouTubePlayer';
import ArcReactor from './ArcReactor';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: Date;
  onSpeak?: (text: string) => void;
  videoId?: string;
  isThinking?: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  isUser,
  timestamp,
  onSpeak,
  videoId,
  isThinking = false,
}) => {
  const { colorMode } = useColorMode();
  const [showVideo, setShowVideo] = useState(true);

  const handleVideoError = () => {
    setShowVideo(false);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Flex
      justify={isUser ? 'flex-end' : 'flex-start'}
      mb={6}
      width="100%"
      px={4}
      alignItems="flex-start"
      gap={2}
    >
      {!isUser && (
        <VStack align="center" spacing={7} flexShrink={0} mr={2}>
          <Box 
            w="24px" 
            h="24px" 
            transform="scale(0.24)"
            transformOrigin="center"
            position="relative"
          >
            <ArcReactor isThinking={isThinking} />
          </Box>
          <Text
            fontSize="xs"
            color={colorMode === 'light' ? 'gray.600' : 'gray.400'}
            mt="-40px"
          >
            {formatTime(timestamp)}
          </Text>
        </VStack>
      )}

      <Flex 
        p={videoId ? 2 : 4}
        borderRadius="lg"
        bg={isUser 
          ? (colorMode === 'light' ? 'blue.50' : 'blue.900')
          : (colorMode === 'light' ? 'gray.100' : 'gray.700')
        }
        color={colorMode === 'light' ? 'gray.800' : 'white'}
        width={videoId ? "100%" : "auto"}
        maxW={isUser ? "80%" : "100%"}
        align="center"
        gap={2}
        flexGrow={1}
        mt={!isUser ? "35px" : "0"}
      >
        {videoId && showVideo ? (
          <YouTubePlayer
            videoId={videoId}
            onError={handleVideoError}
          />
        ) : (
          <>
            <Text whiteSpace="pre-wrap" flex="1">{message}</Text>
            {!isUser && onSpeak && (
              <IconButton
                aria-label="Speak message"
                icon={<FaVolumeUp />}
                size="sm"
                colorScheme="blue"
                variant="ghost"
                onClick={() => onSpeak(message)}
              />
            )}
          </>
        )}
      </Flex>

      {isUser && (
        <VStack align="center" spacing={7} flexShrink={0} ml={2}>
           <Text
            fontSize="xs"
            color={colorMode === 'light' ? 'gray.600' : 'gray.400'}
            mb="-16px"
          >
            {formatTime(timestamp)}
          </Text>
           <IconButton
              aria-label="User"
              icon={<FaUser />}
              size="sm"
              colorScheme="blue"
              isRound
            />
        </VStack>
      )} 

    </Flex>
  );
};

export default ChatMessage; 