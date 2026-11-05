

export default async function StudentDetails({params, }: {params: Promise<{id: string}>}){
    const {id} = await params

    await new Promise((resolve) =>
        setTimeout(resolve, 1000)
    )

    return(
        <div>
            hai student {id}
        </div>
    )
}