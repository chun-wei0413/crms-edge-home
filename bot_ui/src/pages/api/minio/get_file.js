import * as Minio from 'minio'

const minioClient = new Minio.Client({
    endPoint: "minio",
    port: 9000,
    useSSL: false,
    accessKey: "DefaultUser",
    secretKey: "DefaultPassword"
});
export default async function handler(req, res) {
    if (req.method === 'GET') {
        try {
            const { bucket, filename } = req.query;
            const dataStream = await minioClient.getObject(bucket, filename);
            dataStream.pipe(res);
        } catch (error) {
            res.status(500).json({ error: 'Unable to fetch file', details: error });
        }
    } else {
        res.status(405).json({ error: 'Method Not Allowed' });
    }
}
