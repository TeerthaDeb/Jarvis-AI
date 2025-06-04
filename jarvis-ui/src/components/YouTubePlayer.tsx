import React, { useEffect, useState } from 'react';
import { Box, Text, useColorMode } from '@chakra-ui/react';

interface YouTubePlayerProps {
  videoId: string;
  onEnd?: () => void;
  onError?: () => void;
}

const YouTubePlayer: React.FC<YouTubePlayerProps> = ({ videoId, onEnd, onError }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const { colorMode } = useColorMode();

  useEffect(() => {
    setIsLoading(true);
    setHasError(false);
  }, [videoId]);

  const handleError = () => {
    setHasError(true);
    setIsLoading(false);
    onError?.();
  };

  if (hasError) {
    return (
      <Box
        p={4}
        bg={colorMode === 'light' ? 'red.50' : 'red.900'}
        borderRadius="lg"
        textAlign="center"
      >
        <Text color={colorMode === 'light' ? 'red.600' : 'red.200'}>
          Failed to load video. Please try again.
        </Text>
      </Box>
    );
  }

  return (
    <Box
      position="relative"
      width="100%"
      maxWidth="640px"
      margin="0 auto"
      paddingTop="56.25%"
      borderRadius="lg"
      overflow="hidden"
      boxShadow="xl"
      bg={colorMode === 'light' ? 'gray.100' : 'gray.800'}
      minHeight="360px"
      border="1px solid"
      borderColor={colorMode === 'light' ? 'gray.200' : 'gray.600'}
    >
      {isLoading && (
        <Box
          position="absolute"
          top="50%"
          left="50%"
          transform="translate(-50%, -50%)"
          zIndex={1}
          bg={colorMode === 'light' ? 'white' : 'gray.800'}
          p={4}
          borderRadius="md"
          boxShadow="md"
        >
          <Text fontSize="lg">Loading video...</Text>
        </Box>
      )}
      <iframe
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          border: 'none',
          zIndex: 2,
        }}
        src={`https://www.youtube.com/embed/${videoId}?autoplay=1&enablejsapi=1&origin=${window.location.origin}&rel=0`}
        title="YouTube video player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        onLoad={() => setIsLoading(false)}
        onError={handleError}
      />
    </Box>
  );
};

export default YouTubePlayer; 