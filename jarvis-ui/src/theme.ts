import { extendTheme } from '@chakra-ui/react';
import type { ThemeConfig } from '@chakra-ui/theme';

const config: ThemeConfig = {
  initialColorMode: 'dark',
  useSystemColorMode: true,
};

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: {
        bg: 'gray.900',
        color: 'white',
      },
    },
  },
  components: {
    Container: {
      baseStyle: {
        maxW: 'container.md',
      },
    },
  },
});

export default theme; 