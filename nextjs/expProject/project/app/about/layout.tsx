import {ReactNode} from "react";

export default function aboutLayout({children}: {children: ReactNode}) {
    return(
        <div>
            <div>About header</div>
            {children}
            <div>about footer</div>
        </div>
    )
}