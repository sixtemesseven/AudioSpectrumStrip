#include <string.h>
#include "ws2812_led.h"


struct pixel {
    uint8_t g;
    uint8_t r;
    uint8_t b;
};

struct pixel channel_framebuffers[1][900];


int serialLed(void)
{
	uint8_t txBuf[2] = {'A', '\n'};
	CDC_Transmit_FS(txBuf, sizeof(txBuf));

    struct led_channel_info led_channels[1];

    __enable_irq();
    HAL_Delay(200);

    /* Populate the led_channel_info structure. Set the framebuffer pointer for each channel,
     * and the length of the framebuffer for that channel. Lengths are in bytes, NOT in pixels.
     * We allow some framebuffers to be shorter than others (ie, if your LED strips are of
     * unequal lengths) without wasting memory. Removing the length check from ws2812_refresh()
     * will improve performance, but we are within spec as-is.
     */
    for (int i = 0; i < 1; i++) {
        led_channels[i].framebuffer = channel_framebuffers[i];
        led_channels[i].length = FRAMEBUFFER_SIZE * sizeof(struct pixel);
    }

    ws2812_init();

    while(1) {
    	while(1)
    	{
    		if(dataInBuffer > 0)
    		{
    		uint8_t txBuf[2] = {'B', '\n'};
    		CDC_Transmit_FS(txBuf, sizeof(txBuf));
    		CDC_Transmit_FS(buffer, dataInBuffer);
    		if(1) //buffer[0] == 0xff) //Check Start Byte ok
    		{
    			uint32_t len = buffer[1] + (buffer[2] << 8); //Lenght of packet
    			uint8_t channel = buffer[4]; // Channel
    			int j = 0;

    			for(int i = 4; i < (len + 4); i++)
    			{
    				channel_framebuffers[channel][i].r = buffer[j++];
    				channel_framebuffers[channel][i].g = buffer[j++];
    				channel_framebuffers[channel][i].b = buffer[j++];
    			}

    			__disable_irq();
    			ws2812_refresh(led_channels, GPIOB);
    			__enable_irq();
    			uint8_t txBuf[2] = {'C', '\n'};
    			CDC_Transmit_FS(txBuf, sizeof(txBuf));

    			break;
    		}
    	}
    }
}
}


