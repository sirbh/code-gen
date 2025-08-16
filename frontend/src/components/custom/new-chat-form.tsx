import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select"
import { Textarea } from "../ui/textarea"
import axios from "axios"
import { useRouter } from "next/navigation"
import { useContext, useEffect, useState } from "react"
import { ChatStateContext } from "@/context/chat-state"



const formSchema = z.object({
    name: z.string().min(1, "Name is required"),
    age: z
        .string()
        .min(1, "Age is required")
        .refine((val) => !isNaN(Number(val)) && Number(val) > 0, {
            message: "Age must be a positive number",
        }),
    gender: z.enum(["male", "female", "other"], {
        required_error: "Gender is required",
    }),
    conditions: z
        .string()
        .optional()
});




export default function NewChatForm() {

    const router = useRouter()
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            age: "",
            conditions: "",
            gender: "female"

        },
    })

    const [loading, setLoading] = useState(false);

    const { addChat } = useContext(ChatStateContext);

    const getProfileDetails = async () => {
        try {
            setLoading(true);
            const res = await axios.get('/api/user-profile', {
                withCredentials: true,
            });
            setLoading(false);
            if (res.data) {
                form.setValue('name', res.data.user_name || '');
                form.setValue('age', res.data.age.toString() || '');
                form.setValue('gender', res.data.gender || 'female');
                const conditions = Array.isArray(res.data.conditions)
                    ? res.data.conditions.join(', ')
                    : res.data.conditions || '';
                form.setValue('conditions', conditions);
            }
        } catch (error) {
            setLoading(false);
            console.error('Error fetching profile details:', error);
        }
    }

    useEffect(() => {
        getProfileDetails();
    }, [])

    async function onSubmit(values: z.infer<typeof formSchema>) {

        const resp = await axios.post('/api/new-chat', values, {
            withCredentials: true,
        })

        console.log('Form values:', values);

        addChat?.({
            chat_id: resp.data.chatId,
            info: { name: resp.data.info.name }
        });

        router.push(`/${resp.data.chatId}`)

    }
    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="h-fit flex flex-col gap-4 w-sm p-4 bg-card shadow-sm rounded-lg">
                <div className="flex gap-4">
                    <div className="flex-1">
                        <FormField
                            control={form.control}
                            name="name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Name</FormLabel>
                                    <FormControl>
                                        <Input placeholder="Enter Name" {...field} />
                                    </FormControl>
                                    <FormDescription>
                                        Enter patient&apos;s name
                                    </FormDescription>
                                    <FormMessage className="min-h-4" />
                                </FormItem>
                            )}
                        />
                    </div>
                    <div className="flex-1">
                        <FormField
                            control={form.control}
                            name="age"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Age</FormLabel>
                                    <FormControl>
                                        <Input placeholder="Enter Age" {...field} />
                                    </FormControl>
                                    <FormDescription>
                                        Enter age in years
                                    </FormDescription>
                                    <FormMessage className="min-h-4" />
                                </FormItem>
                            )}
                        />
                    </div>

                </div>
                <FormField
                    control={form.control}
                    name="gender"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Gender</FormLabel>
                            <FormControl>
                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                    <SelectTrigger className="w-full">
                                        <SelectValue placeholder="Select gender" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="male">Male</SelectItem>
                                        <SelectItem value="female">Female</SelectItem>
                                        <SelectItem value="other">Other</SelectItem>
                                    </SelectContent>
                                </Select>
                            </FormControl>
                            <FormDescription>
                                Select Gender
                            </FormDescription>
                            <FormMessage className="min-h-4" />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="conditions"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Known Conditions</FormLabel>
                            <FormControl>
                                <Textarea placeholder="e.g., diabetes, hypertension" {...field} />
                            </FormControl>
                            <FormDescription>
                                Enter any known medical conditions
                            </FormDescription>
                            <FormMessage className="min-h-4" />
                        </FormItem>
                    )}
                />
                <Button type="submit" disabled={loading} className="w-full">Start New Chat</Button>
            </form>
        </Form>
    )
}