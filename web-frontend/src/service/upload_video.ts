export const UploadVideo = async (serviceUrl: string, file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${serviceUrl}/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Upload failed: ${errorText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error uploading video:', error);
        throw error;
    }
};