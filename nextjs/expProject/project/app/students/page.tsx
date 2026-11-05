import Link from "next/link";

export default function students(){
    return(
        <div>
            This is the student directory

            student 1: <Link href="students/100">details</Link>
        </div>
    )
}