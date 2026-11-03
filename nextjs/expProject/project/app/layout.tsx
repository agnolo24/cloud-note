import {ReactNode} from "react";

export default function rootLayout({children}: {children: ReactNode}){
    return(
        <html>
        <body className="bg-black text-white">
            {children}
        </body>
        </html>
    )
}