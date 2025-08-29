import "@/app/globals.css"
import 'react-toastify/dist/ReactToastify.css';
import React, {useEffect, useState} from "react";
import {toast, ToastContainer} from "react-toastify";
import {GetServerSideProps} from "next";
import {UploadVideo} from "@/service/upload_video";
import Link from "next/link";
export interface ClientServiceProps{
    serviceUrl:string
}
const fetchFiles = async (bucket:string) => {
    try {
        const response = await fetch('/api/minio/list_files?bucket='+bucket);
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();
        return data
    } catch (error) {
        console.error('Error:', error);
    }
};
const fetchFile = async (src:string) => {
    try {
        const response = await fetch(src);
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();
        return data["url"]
    } catch (error) {
        console.error('Error:', error);
    }
};

export const getServerSideProps: GetServerSideProps = async () => {
    const serviceUrl=process.env.API_URL || "http://localhost:5000";
    return {props:{serviceUrl}};
}
const Home: React.FC<ClientServiceProps> = ({serviceUrl}) => {
    const [originalItem,setOriginalItem]=useState([])
    const [resultItem,setResultItem]=useState([])
    const [playResource,setPlayResource]=useState("")
    const [file, setFile] = useState<File|null>(null);
    const [submitEnable,setSubmitEnable]=useState(true);

    const uploadVideo=()=>{
        if (file===null){
            toast.warn("影片資源 不得為空")
            return
        }
        setSubmitEnable(false)
        toast.promise(
            UploadVideo(serviceUrl,file),
            {
                pending: {
                    render() {
                        return `上傳中......`
                    },
                    icon: false,
                },
                success: {
                    render() {
                        setSubmitEnable(true)
                        setFile(null)
                        return `上傳成功`
                    },
                },
                error: {
                    render({data}) {
                        setSubmitEnable(true)
                        return `上傳失敗 ${data}`
                    },
                }
            }
        ).then(
            ()=>{
                fetchFiles("uploads").then((r)=>{if (r!==undefined)setOriginalItem(r)})
                fetchFiles("results").then((r)=>{if (r!==undefined)setResultItem(r);})
            }
        ).catch((e)=>{console.log(e)})
    }

    useEffect(() => {
            fetchFiles("uploads").then((r)=>{if (r!==undefined)setOriginalItem(r)})
            fetchFiles("results").then((r)=>{if (r!==undefined)setResultItem(r);})
        }
        ,[])
    return (
        <main className={"w-screen h-screen p-1 flex flex-col"}>
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="light"/>
            <div className={"w-full rounded border-2 border-blue-200 flex justify-evenly pt-5 pb-5"}>
                <p className={"text-2xl font-bold text-center"}>上傳影片</p>
                <div className={"relative border-none bg-opacity-50 overflow-hidden"}>
                    <input onChange={(e)=>setFile(e.target.files!.item(0))} accept={"video/mp4"} multiple={false} type={"file"} className={" w-full h-full"}/>
                </div>
                <div className={"justify-center flex flex-row items-center"}>
                    <button onClick={uploadVideo} className={"text-lg font-bold rounded-xl"}>送出</button>
                </div>
            </div>
            <div className={"flex flex-row h-full"}>
                <div className={"flex-1 rounded border-2 border-blue-200 h-full"}>
                    <p className={"text-2xl font-bold text-center"}>原始影片</p>
                    <div className={"grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 p-1"}>
                        {originalItem.map((item,index)=>{
                            if (String(item["name"]).includes("-thumbnail.jpg")) {
                                return(
                                    <img width={200} height={200} className={"truncate w-full"} key={index}
                                         src={serviceUrl+"/media/uploads/file/"+item["name"]}
                                         onClick={()=>{setPlayResource(serviceUrl+"/media/uploads/file/"+originalItem[index-1]["name"])}}></img>
                                )
                            }
                        })}
                    </div>
                </div>
                <div className={"flex-1 rounded border-2 border-blue-200 h-full"}>
                    <p className={"text-2xl font-bold text-center"}>處理後影片</p>
                    <div className={"grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 p-1"}>
                        {resultItem.map((item,index)=>{
                            if (String(item["name"]).includes("-thumbnail.jpg")) {
                                return(
                                    <img width={200} height={200} className={"truncate w-full"} key={index}
                                         src={serviceUrl+"/media/results/file/"+item["name"]}
                                         onClick={()=>{setPlayResource(serviceUrl+"/media/results/file/"+String(item["name"]).substring(0,String(item["name"]).indexOf("-thumbnail.jpg")))}}></img>
                                )
                            }
                        })}
                    </div>
                </div>
            </div>
            {playResource===""?
                <div></div>:
                <div className={"absolute w-screen h-screen flex justify-center align-middle items-center flex-col"}>
                    <div className={"w-2/3 bg-black p-2 rounded"}>
                        <div className={"w-full flex justify-evenly mb-1"}>
                            <Link className={"text-white font-bold text-lg"} href={playResource}>直接下載</Link>
                            <button className={"font-bold text-lg text-white"} onClick={()=>{setPlayResource("")}}>關閉</button>
                        </div>
                        <video controls className={"w-full rounded"} src={playResource}></video>

                    </div>
                </div>
            }
        </main>
    );
}

export default Home;